"""nemotron-nav-agent: A* planning + go-to-goal tracking, supervised by an
NVIDIA Nemotron model on Nebius Token Factory.

Three subcommands:

    python main.py run                 # plan + track on the canonical map
    python main.py run --gif           # ... and record docs/demo.gif
    python main.py tune                # let the model tune the tracker
    python main.py evaluate            # the full evaluation, three tables
    python main.py evaluate --mock     # ... without calling the API

This file is short on purpose -- it does not implement any algorithm. It
wires modules together. The algorithms live in ``src/``, each in its own
file: the planner, the controller, the metrics, the client, the agent.
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.agent import NavAgent                                       # noqa: E402
from src.metrics import measure                                      # noqa: E402
from src.nebius_client import TokenFactory                           # noqa: E402
from src.simulation import build_world, describe                     # noqa: E402

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def cmd_run(args):
    """Plan and track on the canonical map, then show it."""
    world = build_world(tol=args.tol, speed=args.speed, Kp=args.kp)
    print(describe(world))
    m = measure(world)
    print(f"max cross-track : {m['max_cross_track_m']:.4f} m")
    print(f"mean cross-track: {m['mean_cross_track_m']:.4f} m")
    print(f"end-point error : {m['end_point_error_m']:.4f} m")
    print(f"time            : {m['time_s']:.2f} s")

    if args.gif:
        from src.render import record_gif
        frames, nbytes = record_gif(world, args.out)
        print(f"GIF: {args.out}  {frames} frames  {nbytes / 1024 / 1024:.2f} MB")
    elif not args.no_view:
        # The live window needs pygame. It is the one optional dependency in
        # this project, so a missing pygame must degrade to a note, not a
        # traceback -- otherwise "python main.py run" fails on a machine
        # that has everything the simulation itself needs.
        #
        # The import has to be probed here rather than inside src/viewer.py:
        # that module imports cleanly without pygame and only needs it when
        # the window is actually opened, so the ImportError would surface
        # later than it is caught here.
        try:
            import pygame  # noqa: F401
        except ImportError:
            print("\npygame is not installed, so the live window is unavailable. "
                  "Nothing else is affected: the run above is complete, and "
                  "'python main.py run --gif' records the video with numpy + "
                  "Pillow alone.")
        else:
            from src.viewer import play
            play(world)


def cmd_tune(args):
    """Let the model read the metrics and adjust the controller."""
    client = TokenFactory(model=args.model, mock=True if args.mock else None)
    if client.mock:
        print("mock mode: the pipeline and every measured number are real; "
              "only the suggestions come from fixed rules.\n")
    else:
        print(f"live mode: {client.model}\n")

    agent = NavAgent(client, model=args.model)
    result = agent.autotune(
        instruction="Move the robot from cell (1,1) to cell (8,8), "
                    "going around the wall in the middle.",
        task={"start": [1, 1], "goal": [8, 8]},
        rounds=args.rounds,
    )

    print()
    print("Every decision the model made, in order:")
    n = 0
    for step in agent.trace:
        if step.get("step") == "diagnose" and "result" in step:
            n += 1
            r = step["result"]
            print(f"  {n}. {r['diagnosis']}")
            print(f"     -> {r['changes'] if r['changes'] else 'no change'} "
                  f"(confidence {r['confidence']:.2f})")
    print()
    print(f"best: {result['best_params']}")
    print(f"      max cross-track {result['best_metrics']['max_cross_track_m']:.4f} m, "
          f"time {result['best_metrics']['time_s']:.2f} s")


def cmd_evaluate(args):
    """Run the full evaluation and print the three tables."""
    import tools.agent_eval as ae

    if args.mock:
        sys.argv = ["agent_eval", "--mock"]
    else:
        sys.argv = ["agent_eval"]
    if args.maps:
        sys.argv += ["--maps", str(args.maps)]
    ae.main()


def main():
    ap = argparse.ArgumentParser(
        description="nemotron-nav-agent: A* planning + go-to-goal tracking "
                    "with an LLM supervision layer")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_run = sub.add_parser("run", help="plan + track on the canonical map")
    p_run.add_argument("--gif", action="store_true", help="record a GIF instead of opening a window")
    p_run.add_argument("--no-view", action="store_true", help="do not open a window at all")
    p_run.add_argument("--tol", type=float, default=0.05, help="waypoint tolerance (m)")
    p_run.add_argument("--speed", type=float, default=0.5, help="forward speed (m/s)")
    p_run.add_argument("--kp", type=float, default=5.0, help="heading gain")
    p_run.add_argument("--out", default=os.path.join(BASE_DIR, "docs", "demo.gif"))
    p_run.set_defaults(func=cmd_run)

    p_tune = sub.add_parser("tune", help="let the model tune the tracker")
    p_tune.add_argument("--mock", action="store_true", help="force mock mode")
    p_tune.add_argument("--rounds", type=int, default=3, help="tuning rounds")
    p_tune.add_argument("--model", default=None, help="override the model id")
    p_tune.set_defaults(func=cmd_tune)

    p_eval = sub.add_parser("evaluate", help="the full evaluation, three tables")
    p_eval.add_argument("--mock", action="store_true", help="force mock mode")
    p_eval.add_argument("--maps", type=int, default=None, help="number of random maps")
    p_eval.set_defaults(func=cmd_evaluate)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
