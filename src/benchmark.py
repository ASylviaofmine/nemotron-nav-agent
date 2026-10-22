"""Multi-map evaluation: does the agent work on maps it was never tuned on?

A single map is an anecdote. A reviewer will ask the obvious next question:
"does your agent still work when the map changes?" This module answers it
by running the agent over a suite of randomly generated maps and reporting
the distribution, not just the average.

The suite is deterministic -- seeded with a fixed value, so the numbers in
the README can be regenerated exactly. Two families of map are used:

* **wall maps** -- the canonical layout: a wall across the middle with a
  few openings, so the robot has to detour.
* **random maps** -- uniform random obstacles at a given density, filtered
  to keep only those whose start and goal are actually connected (an
  unreachable map would make the run fail rather than fail *badly*).

For each map the agent is given the same starting parameters and the same
budget of rounds, and the outcome is recorded. The summary reports the
median and worst case of the improvement, because "the average improved by
40%" hides a scenario where the agent made things worse.
"""

import numpy as np

from src.agent import NavAgent
from src.metrics import measure
from src.simulation import build_world

DEFAULT_SIZE = 10
DEFAULT_START = (1, 1)
DEFAULT_GOAL = (8, 8)
BASE_PARAMS = {"tol": 0.05, "speed": 0.5, "Kp": 5.0}

# The prior-knowledge control: the tuning knowledge the model's system
# prompt spells out, applied as a fixed rule with no model in the loop.
# Without this row, "the agent improved the map" would not distinguish a
# model that reasoned from a script that guessed well.
HEURISTIC_PARAMS = {"tol": 0.05, "speed": 0.5, "Kp": 12.0}


def make_wall_map(size=DEFAULT_SIZE, wall_row=None, openings=None):
    """The canonical layout: one horizontal wall with a few gaps.

    ``openings`` are the column indices left free in the wall row.
    Defaults to the two outermost columns, which is the layout used in the
    README and the demo video.
    """
    from src.grid import Grid

    if openings is None:
        openings = (0, size - 1)

    grid = Grid(size)
    row = size // 2 if wall_row is None else wall_row
    for c in range(size):
        if c not in openings:
            grid.set_wall(row, c)
    return grid


def make_random_map(size, density, rng):
    """Uniform random obstacles. Returns a Grid (may be disconnected)."""
    from src.grid import Grid

    grid = Grid(size)
    for r in range(size):
        for c in range(size):
            if rng.random() < density:
                grid.set_wall(r, c)
    return grid


def is_connected(grid, start, goal):
    """Is there any path from start to goal? Uses the planner itself."""
    from src.planner import astar

    return astar(grid, start, goal) is not None


def build_suite(n_random=8, size=DEFAULT_SIZE, density=0.20, seed=42):
    """A deterministic suite of maps, all guaranteed solvable.

    Returns a list of ``(name, grid)`` pairs.
    """
    rng = np.random.default_rng(seed)
    suite = []

    # The canonical map first -- it is the one shown in the README and video.
    suite.append(("wall-map", make_wall_map(size)))

    # A second wall map with the openings moved, so the agent cannot
    # succeed by memorising "always go right".
    suite.append(("wall-map-offset", make_wall_map(size, wall_row=size // 3,
                                                   openings=(size // 2, size - 1))))

    # Random maps, filtered to the solvable ones.
    attempts = 0
    wanted = n_random
    while wanted > 0 and attempts < 500:
        attempts += 1
        grid = make_random_map(size, density, rng)
        if is_connected(grid, DEFAULT_START, DEFAULT_GOAL):
            suite.append((f"random-{wanted:02d}", grid))
            wanted -= 1

    return suite


def run_on_grid(grid, agent, start=DEFAULT_START, goal=DEFAULT_GOAL, rounds=3):
    """Run the agent's tuning loop on one specific grid.

    The grid is injected rather than rebuilt, so the agent meets exactly the
    same obstacle layout the baseline was measured on.
    """
    from src.planner import astar
    from src.grid import cell_to_world
    from src.controller import follow
    from src.metrics import measure_world

    path = astar(grid, start, goal)
    if path is None:
        return None

    waypoints = [cell_to_world(cell) for cell in path]

    def evaluate(params):
        traj, thetas, t = follow(waypoints, tol=params["tol"],
                                 speed=params["speed"], Kp=params["Kp"])
        return measure_world(traj, waypoints, t, len(path))

    baseline = evaluate(BASE_PARAMS)
    heuristic = evaluate(HEURISTIC_PARAMS)

    # The agent's own loop, but with the evaluation function injected so it
    # works on this grid. See src/agent.py -- NavAgent.run_tuning() takes an
    # ``evaluate`` callable for exactly this reason.
    result = agent.run_tuning(evaluate=evaluate, rounds=rounds,
                              start=start, goal=goal)

    return {
        "baseline": baseline,
        "heuristic": heuristic,
        "agent": result["best_metrics"],
        "agent_params": result["best_params"],
        "rounds": result["rounds"],
        "history": result["history"],
    }


def evaluate_suite(agent, suite=None, rounds=3, verbose=True):
    """Run the agent over the whole suite and summarise.

    Returns ``{"rows": [...], "summary": {...}}``.
    """
    if suite is None:
        suite = build_suite()

    rows = []
    for name, grid in suite:
        out = run_on_grid(grid, agent, rounds=rounds)
        if out is None:
            continue

        b, a = out["baseline"], out["agent"]
        h = out["heuristic"]
        rows.append({
            "map": name,
            "baseline_ct": b["max_cross_track_m"],
            "heuristic_ct": h["max_cross_track_m"],
            "agent_ct": a["max_cross_track_m"],
            "baseline_time": b["time_s"],
            "agent_time": a["time_s"],
            "improved": a["max_cross_track_m"] < b["max_cross_track_m"] - 1e-9,
            "regressed": a["max_cross_track_m"] > b["max_cross_track_m"] + 1e-9,
            "beats_heuristic": a["max_cross_track_m"] < h["max_cross_track_m"] - 1e-9,
            "params": out["agent_params"],
        })
        if verbose:
            flag = "improved" if rows[-1]["improved"] else (
                "REGRESSED" if rows[-1]["regressed"] else "unchanged")
            vs_h = "beats control" if rows[-1]["beats_heuristic"] else "ties control"
            print(f"  {name:<18} baseline {b['max_cross_track_m']:.4f} m -> "
                  f"agent {a['max_cross_track_m']:.4f} m   ({flag}, {vs_h})")

    if not rows:
        return {"rows": [], "summary": {}}

    base = np.array([r["baseline_ct"] for r in rows])
    heur = np.array([r["heuristic_ct"] for r in rows])
    ag = np.array([r["agent_ct"] for r in rows])
    ratios = base / np.maximum(ag, 1e-12)

    summary = {
        "n_maps": len(rows),
        "n_improved": sum(1 for r in rows if r["improved"]),
        "n_regressed": sum(1 for r in rows if r["regressed"]),
        "n_unchanged": sum(1 for r in rows if not r["improved"] and not r["regressed"]),
        "n_beats_heuristic": sum(1 for r in rows if r["beats_heuristic"]),
        "median_baseline_ct": float(np.median(base)),
        "median_heuristic_ct": float(np.median(heur)),
        "median_agent_ct": float(np.median(ag)),
        "worst_baseline_ct": float(base.max()),
        "worst_agent_ct": float(ag.max()),
        "median_ratio": float(np.median(ratios)),
        "median_improvement_pct": float((1 - np.median(ag) / np.median(base)) * 100),
        "worst_case_ratio": float(ratios.min()),
    }
    return {"rows": rows, "summary": summary}


def format_summary(summary):
    """A Markdown table plus a one-line verdict."""
    if not summary:
        return "(no results)"

    lines = []
    lines.append("| Metric | Value |")
    lines.append("|---|---|")
    lines.append(f"| Maps evaluated | {summary['n_maps']} |")
    lines.append(f"| Improved over baseline | {summary['n_improved']} |")
    lines.append(f"| Unchanged | {summary['n_unchanged']} |")
    lines.append(f"| Regressed | {summary['n_regressed']} |")
    lines.append(f"| Beat the no-model control | {summary['n_beats_heuristic']} |")
    lines.append(f"| Median baseline cross-track | {summary['median_baseline_ct']:.4f} m |")
    lines.append(f"| Median no-model control | {summary['median_heuristic_ct']:.4f} m |")
    lines.append(f"| Median agent cross-track | {summary['median_agent_ct']:.4f} m |")
    lines.append(f"| Median improvement | {summary['median_improvement_pct']:.1f} % |")
    lines.append(f"| Worst baseline cross-track | {summary['worst_baseline_ct']:.4f} m |")
    lines.append(f"| Worst agent cross-track | {summary['worst_agent_ct']:.4f} m |")
    lines.append(f"| Worst-case improvement ratio | {summary['worst_case_ratio']:.2f}x |")
    return "\n".join(lines)
