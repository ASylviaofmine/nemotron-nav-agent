"""End-to-end evaluation of the Nemotron supervision layer.

Four questions, and the tables that answer them.

1. **Does the pipeline work at all?** -- the canonical map, agent vs the
   fixed baseline.
2. **Is the model doing anything a fixed rule could not?** -- the agent is
   compared against a *prior-knowledge heuristic* that encodes the same
   tuning knowledge the model is given in its system prompt, but applies it
   blindly with no model involved. If the agent cannot beat this, the model
   is decoration, and the table says so.
3. **Does it generalise?** -- the same loop over a suite of random and
   perturbed maps, reporting the distribution rather than one number.
4. **How close is it to optimal?** -- the distance to the best of all swept
   parameter combinations, an independent ground truth that involves no
   model at all.

Table 4 is the one that makes the claim checkable. The sweep is
deterministic, it lives in the repository, and it knows nothing about
Nemotron -- so "the agent reached within X of the best of 125
combinations" is a statement a reviewer can verify by running one script.

Run:

    python tools/agent_eval.py                # live Token Factory calls
    python tools/agent_eval.py --mock         # same pipeline, fixed rules
    python tools/agent_eval.py --maps 12      # more maps in the suite
    python tools/agent_eval.py --model nvidia/nemotron-3-nano-30b-a3b
"""

import argparse
import os
import sys

# Make the project importable when this file is run directly
# ("python tools/agent_eval.py") rather than as a module
# ("python -m tools.agent_eval"). The try/except keeps the import block at
# the top of the file, which is what lets the editor resolve these
# imports without flagging them.
try:
    from tools._bootstrap import ROOT  # noqa: F401
except ImportError:                     # running as a loose script
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agent import NavAgent
from src.benchmark import BASE_PARAMS, build_suite, evaluate_suite, format_summary
from src.metrics import measure
from src.nebius_client import TokenFactory
from src.simulation import build_world

# The exhaustive reference set: 5 x 5 x 5 = 125 combinations.
SWEEP = {
    "tol": [0.02, 0.05, 0.10, 0.20, 0.30],
    "speed": [0.30, 0.50, 0.80, 1.00, 1.50],
    "Kp": [2.0, 3.0, 5.0, 8.0, 12.0],
}

# The prior-knowledge control. This is the tuning knowledge that the
# model's system prompt spells out, applied as a fixed rule with no model
# in the loop at all. It exists so that "the model helped" is a claim that
# can be falsified rather than a claim that is true by construction.
HEURISTIC_PARAMS = {"tol": 0.05, "speed": 0.5, "Kp": 12.0}


def evaluate_canonical(params, start=(1, 1), goal=(8, 8)):
    world = build_world(size=10, start=start, goal=goal,
                        tol=params["tol"], speed=params["speed"], Kp=params["Kp"])
    return measure(world)


def exhaustive_best(start=(1, 1), goal=(8, 8)):
    """Best of all 125 swept combinations -- the independent ground truth."""
    best = None
    for tol in SWEEP["tol"]:
        for speed in SWEEP["speed"]:
            for kp in SWEEP["Kp"]:
                m = evaluate_canonical({"tol": tol, "speed": speed, "Kp": kp}, start, goal)
                if best is None or (m["max_cross_track_m"], m["time_s"]) < \
                        (best[1]["max_cross_track_m"], best[1]["time_s"]):
                    best = ({"tol": tol, "speed": speed, "Kp": kp}, m)
    return best


def fmt_params(p):
    return f"tol={p['tol']}, speed={p['speed']}, Kp={p['Kp']}"


def main():
    ap = argparse.ArgumentParser(description="Evaluate the Nemotron nav agent")
    ap.add_argument("--mock", action="store_true", help="force mock mode (no API calls)")
    ap.add_argument("--maps", type=int, default=8, help="number of random maps in the suite")
    ap.add_argument("--rounds", type=int, default=3, help="tuning rounds per map")
    ap.add_argument("--model", default=None, help="override the model id")
    args = ap.parse_args()

    client = TokenFactory(model=args.model, mock=True if args.mock else None)
    print(f"mode: {'mock' if client.mock else 'live'}   model: {client.model}")
    if client.mock:
        print("  (no API key / --mock: the pipeline and every measured number are real;")
        print("   only the suggestions come from fixed rules. The agent rows below are")
        print("   therefore IDENTICAL to the prior-knowledge control by construction --")
        print("   run without --mock for the rows that mean something.)\n")

    agent = NavAgent(client, model=args.model)

    # ---------------------------------------------------- 1. canonical map
    print("## 1. The canonical map\n")
    baseline = evaluate_canonical(BASE_PARAMS)
    heuristic = evaluate_canonical(HEURISTIC_PARAMS)
    print(f"  baseline : {fmt_params(BASE_PARAMS)} -> "
          f"max_ct={baseline['max_cross_track_m']:.4f} m, time={baseline['time_s']:.2f} s")
    print(f"  heuristic: {fmt_params(HEURISTIC_PARAMS)} -> "
          f"max_ct={heuristic['max_cross_track_m']:.4f} m, time={heuristic['time_s']:.2f} s "
          f"(prior-knowledge control, no model involved)")

    result = agent.autotune(instruction="Move the robot from cell (1,1) to cell (8,8), "
                                        "going around the wall in the middle.",
                            task={"start": [1, 1], "goal": [8, 8]},
                            rounds=args.rounds)
    best = result["best_metrics"]
    print(f"  agent    : {fmt_params(result['best_params'])} -> "
          f"max_ct={best['max_cross_track_m']:.4f} m, time={best['time_s']:.2f} s")
    print(f"  improvement: {baseline['max_cross_track_m']:.4f} -> "
          f"{best['max_cross_track_m']:.4f} m "
          f"({(1 - best['max_cross_track_m'] / baseline['max_cross_track_m']) * 100:.1f} %)")
    print(f"  vs the no-model control: {heuristic['max_cross_track_m']:.4f} -> "
          f"{best['max_cross_track_m']:.4f} m "
          f"({(1 - best['max_cross_track_m'] / heuristic['max_cross_track_m']) * 100:+.1f} %)\n")

    # ---------------------------------------------------- 2. generalisation
    print(f"## 2. Generalisation over a suite of maps\n")
    suite = build_suite(n_random=args.maps)
    print(f"  suite: {len(suite)} maps "
          f"({', '.join(n for n, _ in suite[:3])}, ...)\n")
    suite_out = evaluate_suite(agent, suite=suite, rounds=args.rounds, verbose=True)
    print()
    print(format_summary(suite_out["summary"]))
    print()

    # ---------------------------------------------------- 3. vs exhaustive
    print("## 3. Distance to the exhaustive optimum\n")
    opt_p, opt_m = exhaustive_best()
    gap = best["max_cross_track_m"] - opt_m["max_cross_track_m"]
    n_combos = len(SWEEP["tol"]) * len(SWEEP["speed"]) * len(SWEEP["Kp"])
    print("| Reference | Max cross-track (m) | Time (s) | Parameters |")
    print("|---|---|---|---|")
    print(f"| Fixed baseline | {baseline['max_cross_track_m']:.4f} | "
          f"{baseline['time_s']:.2f} | {fmt_params(BASE_PARAMS)} |")
    print(f"| Prior-knowledge control (no model) | {heuristic['max_cross_track_m']:.4f} | "
          f"{heuristic['time_s']:.2f} | {fmt_params(HEURISTIC_PARAMS)} |")
    print(f"| **Nemotron agent** | **{best['max_cross_track_m']:.4f}** | "
          f"{best['time_s']:.2f} | {fmt_params(result['best_params'])} |")
    print(f"| Exhaustive best of {n_combos} | {opt_m['max_cross_track_m']:.4f} | "
          f"{opt_m['time_s']:.2f} | {fmt_params(opt_p)} |")
    print()
    print(f"Agent gap to the exhaustive optimum: {gap:+.4f} m "
          f"(0.0000 would mean it matched the best of {n_combos} combinations).")
    print()
    print("The exhaustive sweep is deterministic, lives in this repository, and")
    print("involves no model at all -- so this row is an independent check on")
    print("the agent, not a restatement of what the agent did.")


if __name__ == "__main__":
    main()
