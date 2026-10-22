"""The supervision layer: an NVIDIA Nemotron model inside a control loop.

The classical half of this project (A* planning, go-to-goal tracking) does
not know anything about language models. This module is where the two meet.

The loop looks like this:

    natural-language task
            |
            v
      plan_task()      Nemotron -> {start, goal, tol, speed, Kp}
            |
            v
      plan -> drive -> measure
                        (max/mean cross-track error, end-point error, time)
            |
            v
      diagnose()       Nemotron -> a diagnosis + proposed parameter changes
            |
            v
      re-run with the new parameters
            |
            v
      keep the change only if the measured numbers improved

Three design decisions worth stating, because they are what separate this
from a chatbot wrapped around a simulator:

1. **The model supervises; it does not steer.** A* still plans the route and
   the controller still drives the robot. The model decides *parameters* and
   *which error to fix next*. It is never asked to invent robot physics.

2. **Every suggestion is falsifiable.** A proposed change is clamped to a
   legal range, applied, and then the simulation is re-run. The measured
   numbers decide whether it was kept. "The model said it would help" is
   never the claim -- the before/after table is.

3. **Metrics reach the model as prose, not as a table.** Sentences like
   "max cross-track error: 0.0895 m" carry the magnitude relationships
   better than a markdown table does.

The model is given the tuning knowledge that was measured on this exact
simulator, in its system prompt. That is a deliberate scoping choice: it
is asked to apply a known trade-off structure to a specific measurement --
a judgement task with a checkable answer -- not to discover control theory.
Its judgement is then checked against an exhaustive parameter sweep
(see ``src/benchmark.py`` and ``tools/agent_eval.py``).

With no API key configured the whole pipeline still runs: the client falls
back to a mock mode in which the *pipeline and every measured number* are
real, and only the suggestions come from fixed rules. That makes the
system reviewable before an account exists.
"""

import copy

from src.metrics import format_metrics
from src.simulation import build_world

# Legal ranges for the controller parameters. Model output is clamped to
# these before use -- a suggestion like "Kp = 500" produces a run that means
# nothing.
BOUNDS = {
    "tol": (0.01, 0.50),
    "speed": (0.10, 2.00),
    "Kp": (0.50, 20.0),
}

DEFAULT_TASK = {
    "start": [1, 1],
    "goal": [8, 8],
    "tol": 0.05,
    "speed": 0.5,
    "Kp": 5.0,
}

TASK_SYSTEM = """You translate a robot navigation task into a JSON parameter set.

The robot is a differential-drive vehicle on a 10x10 grid. Row and column
indices run 0..9. A wall runs across the middle of the grid with only two
openings, so the robot has to detour to reach the far side.

Return ONLY a JSON object with exactly these keys:
  "start": [row, col]        integer pair, the start cell
  "goal":  [row, col]        integer pair, the goal cell
  "tol":   number in [0.01, 0.50]   metres; how close counts as "reached"
  "speed": number in [0.10, 2.00]   metres per second
  "Kp":    number in [0.50, 20.0]    heading gain

Guidance:
  - A tight "tol" buys end-point accuracy but costs a little time.
  - Higher "speed" saves time but increases cross-track error.
  - Higher "Kp" reduces cross-track error at no time cost.
Do not add any commentary outside the JSON."""


DIAGNOSE_SYSTEM = """You are a robotics engineer tuning a wheeled robot's
closed-loop path tracker. You are given the measured metrics of one run and
must diagnose the dominant error source and propose parameter changes.

Return ONLY a JSON object with exactly these keys:
  "diagnosis":  one or two sentences naming the dominant error source
  "changes":    an object holding only the parameters you want to change,
                with keys drawn from "tol", "speed", "Kp" and numeric values
  "confidence": number in [0,1]

Allowed ranges: tol [0.01,0.50], speed [0.10,2.00], Kp [0.50,20.0].

Tuning knowledge (measured on this exact simulator):
  - The heading gain Kp is the cheapest accuracy win. Raising it reduces
    max cross-track error substantially with no time penalty.
  - Speed is the only knob that buys time, and it is paid for in fidelity:
    max cross-track error grows roughly linearly with speed.
  - tol controls end-point error but does NOT reduce cross-track error.

Change at most two parameters. If the metrics are already good, return an
empty "changes" object. Do not add commentary outside the JSON."""


def _better(a, b):
    """Metric comparison: smaller cross-track wins, ties broken by time.

    Cross-track error comes first because the point of this project is
    "the robot follows the path it was given", not "the robot arrives
    quickly". The measurements agree: speed buys time with fidelity.
    """
    return (a["max_cross_track_m"], a["time_s"]) < (b["max_cross_track_m"], b["time_s"])


def _clamp(name, value):
    """Clamp a model-supplied parameter into its legal range."""
    lo, hi = BOUNDS[name]
    try:
        v = float(value)
    except (TypeError, ValueError):
        return None
    if v != v:                                    # NaN
        return None
    return max(lo, min(hi, v))


def _as_cell(value, default):
    """Normalise a model-supplied [row, col] into a legal cell."""
    try:
        r, c = int(value[0]), int(value[1])
    except (TypeError, ValueError, IndexError):
        return tuple(default)
    if not (0 <= r <= 9 and 0 <= c <= 9):
        return tuple(default)
    return (r, c)


class NavAgent:
    """Puts a Nemotron model inside the navigation loop.

    ``client`` is an instance of ``src.nebius_client.TokenFactory``. Pass a
    mock one and the entire pipeline runs offline.
    """

    def __init__(self, client, model=None):
        self.client = client
        self.model = model
        self.trace = []                # every decision, for later inspection

    # ------------------------------------------------------------ task parsing

    def plan_task(self, instruction, task=None):
        """Natural language -> structured task parameters.

        Keys present in ``task`` are overwritten by the model's output; the
        rest are kept. The result can be passed straight to ``build_world``.
        """
        base = copy.deepcopy(DEFAULT_TASK)
        if task:
            base.update(task)

        messages = [
            {"role": "system", "content": TASK_SYSTEM},
            {"role": "user", "content": f"Task: {instruction}"},
        ]
        try:
            out = self.client.chat_json(messages, model=self.model, temperature=0.1)
        except Exception as e:                                   # noqa: BLE001
            self.trace.append({"step": "plan_task", "error": str(e), "fallback": base})
            return base

        planned = {
            "start": list(_as_cell(out.get("start"), base["start"])),
            "goal": list(_as_cell(out.get("goal"), base["goal"])),
            "tol": _clamp("tol", out.get("tol", base["tol"])) or base["tol"],
            "speed": _clamp("speed", out.get("speed", base["speed"])) or base["speed"],
            "Kp": _clamp("Kp", out.get("Kp", base["Kp"])) or base["Kp"],
        }
        self.trace.append({"step": "plan_task", "instruction": instruction, "planned": planned})
        return planned

    # ------------------------------------------------------------ diagnosis

    def diagnose(self, metrics, current):
        """Look at the metrics, diagnose, propose parameter changes.

        Returns ``{"diagnosis", "changes", "confidence"}``; the values in
        ``changes`` are already clamped to their legal ranges.
        """
        prompt = (
            f"Controller parameters in use: tol={current['tol']}, "
            f"speed={current['speed']}, Kp={current['Kp']}\n\n"
            f"Measured metrics of the run:\n{format_metrics(metrics)}\n\n"
            "Diagnose the dominant error source and propose parameter changes."
        )
        messages = [
            {"role": "system", "content": DIAGNOSE_SYSTEM},
            {"role": "user", "content": prompt},
        ]
        try:
            out = self.client.chat_json(messages, model=self.model, temperature=0.1)
        except Exception as e:                                   # noqa: BLE001
            self.trace.append({"step": "diagnose", "error": str(e)})
            return {"diagnosis": f"diagnostic call failed: {e}", "changes": {}, "confidence": 0.0}

        raw_changes = out.get("changes") or {}
        changes = {}
        if isinstance(raw_changes, dict):
            for name in ("tol", "speed", "Kp"):
                if name in raw_changes:
                    v = _clamp(name, raw_changes[name])
                    if v is not None and abs(v - current[name]) > 1e-9:
                        changes[name] = v

        result = {
            "diagnosis": str(out.get("diagnosis", "")).strip(),
            "changes": changes,
            "confidence": float(out.get("confidence", 0.0) or 0.0),
        }
        self.trace.append({"step": "diagnose", "metrics": metrics,
                           "current": dict(current), "result": result})
        return result

    # ------------------------------------------------------------ the loop

    def run_tuning(self, evaluate, rounds=3, start=(1, 1), goal=(8, 8),
                   params=None, verbose=True):
        """The tune-measure-adjust loop, with the evaluation function injected.

        ``evaluate(params) -> metrics`` is supplied by the caller. That
        injection is what lets the same loop run on the canonical map and on
        a suite of random maps, without duplicating the loop logic.

        Returns ``{"best_params", "best_metrics", "rounds", "history"}``.
        """
        current = dict(params) if params else dict(DEFAULT_TASK)

        best = None
        history = []

        for rnd in range(rounds):
            metrics = evaluate(current)
            record = {"round": rnd + 1, "params": dict(current), "metrics": metrics}
            history.append(record)

            if verbose:
                print(f"  round {rnd + 1}: tol={current['tol']} speed={current['speed']} "
                      f"Kp={current['Kp']} -> max_ct={metrics['max_cross_track_m']:.4f} m, "
                      f"time={metrics['time_s']:.2f} s")

            if best is None or _better(metrics, best["metrics"]):
                best = {"params": dict(current), "metrics": metrics}

            advice = self.diagnose(metrics, current)
            record["advice"] = advice
            if verbose:
                print(f"      {advice['diagnosis']}")
                if advice["changes"]:
                    print(f"      proposed: {advice['changes']}")

            if not advice["changes"]:
                if verbose:
                    print("      no further changes proposed - stopping")
                break

            current = {**current, **advice["changes"]}

        return {
            "best_params": best["params"] if best else current,
            "best_metrics": best["metrics"] if best else {},
            "rounds": len(history),
            "history": history,
        }

    def autotune(self, instruction=None, task=None, rounds=3, verbose=True):
        """End-to-end on the canonical map: parse the task, then tune.

        This is the convenience entry point used by the CLI and the demo
        app. For evaluation over many maps use ``run_tuning`` with an
        injected evaluator instead.
        """
        params = self.plan_task(instruction, task) if instruction else dict(DEFAULT_TASK)
        start, goal = tuple(params["start"]), tuple(params["goal"])

        def evaluate(p):
            from src.metrics import measure

            world = build_world(size=10, start=start, goal=goal,
                                tol=p["tol"], speed=p["speed"], Kp=p["Kp"])
            return measure(world)

        result = self.run_tuning(evaluate=evaluate, rounds=rounds,
                                 start=start, goal=goal, params=params,
                                 verbose=verbose)
        result["task"] = params
        return result
