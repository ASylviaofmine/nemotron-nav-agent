"""Gradio demo: drive the robot and watch the model tune the tracker.

    pip install gradio
    python app.py

The demo is deliberately not a toy:

* the *left* panel is a live render of the simulation (the same renderer
  the GIF recorder uses);
* the *right* panel is the model's reasoning, updated round by round, with
  the measured before/after numbers next to each suggestion.

That pairing is the whole point of the project: the model proposes, the
simulator disposes, and you can see both halves of that exchange.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.agent import NavAgent                                       # noqa: E402
from src.controller import follow                                    # noqa: E402
from src.grid import cell_to_world                                   # noqa: E402
from src.metrics import measure_world                               # noqa: E402
from src.nebius_client import TokenFactory                           # noqa: E402
from src.planner import astar                                        # noqa: E402
from src.render import render                                        # noqa: E402
from src.simulation import make_map                                  # noqa: E402


def _world(grid, path, traj, thetas, k):
    """Package a partial run into the shape ``src.render.render`` expects."""
    return {
        "grid": grid,
        "path": path,
        "traj": traj,
        "thetas": thetas,
        "start": path[0],
        "goal": path[-1],
    }


def run_task(start_r, start_c, goal_r, goal_c, tol, speed, Kp, rounds, model_id, use_mock):
    """Run the tuning loop, yielding (frame, log) after every round.

    Yields, rather than returns, so the interface updates live.
    """
    client = TokenFactory(model=model_id, mock=True if use_mock else None)
    agent = NavAgent(client, model=model_id)

    grid = make_map(10)
    path = astar(grid, (int(start_r), int(start_c)), (int(goal_r), int(goal_c)))
    if path is None:
        yield render({"grid": grid, "path": [], "traj": [(0.5, 0.5)],
                      "thetas": [0.0], "start": (0, 0), "goal": (0, 0)}, 1), \
            "That goal is unreachable. Pick another one."
        return
    waypoints = [cell_to_world(c) for c in path]

    def evaluate(p):
        traj, thetas, t = follow(waypoints, tol=p["tol"], speed=p["speed"], Kp=p["Kp"])
        return measure_world(traj, waypoints, t, len(path))

    log = [f"model: {'mock rules' if client.mock else client.model}"]
    current = {"tol": tol, "speed": speed, "Kp": Kp}
    best = None
    frame = None

    for rnd in range(rounds):
        m = evaluate(current)
        traj, thetas, t = follow(waypoints, tol=current["tol"],
                                 speed=current["speed"], Kp=current["Kp"])
        frame = render(_world(grid, path, traj, thetas, len(traj)), len(traj))

        tag = ""
        if best is None or (m["max_cross_track_m"], m["time_s"]) < \
                (best["max_cross_track_m"], best["time_s"]):
            best = m
            tag = "  <- kept"
        log.append(
            f"round {rnd + 1}: tol={current['tol']} speed={current['speed']} "
            f"Kp={current['Kp']}\n"
            f"    max cross-track {m['max_cross_track_m']:.4f} m   "
            f"time {m['time_s']:.2f} s{tag}"
        )
        yield frame, "\n".join(log)

        advice = agent.diagnose(m, current)
        log.append(f"    model: {advice['diagnosis']}")
        if advice["changes"]:
            log.append(f"    change: {advice['changes']}")
            current = {**current, **advice["changes"]}
        else:
            log.append("    model: no further change proposed")
            break

    log.append("")
    log.append(f"best measured: max cross-track {best['max_cross_track_m']:.4f} m, "
               f"time {best['time_s']:.2f} s")
    yield frame, "\n".join(log)


def build_ui():
    import gradio as gr

    with gr.Blocks(title="nemotron-nav-agent") as demo:
        gr.Markdown(
            "# nemotron-nav-agent\n"
            "A* plans the route, a go-to-goal controller drives, and an NVIDIA "
            "Nemotron model on Nebius Token Factory reads the measured error and "
            "proposes the next parameter change. The model supervises; it never "
            "steers. Every suggestion is applied, re-run, and kept only if the "
            "numbers improved."
        )
        with gr.Row():
            with gr.Column():
                start_r = gr.Slider(0, 9, value=1, step=1, label="Start row")
                start_c = gr.Slider(0, 9, value=1, step=1, label="Start column")
                goal_r = gr.Slider(0, 9, value=8, step=1, label="Goal row")
                goal_c = gr.Slider(0, 9, value=8, step=1, label="Goal column")
                tol = gr.Slider(0.01, 0.50, value=0.05, step=0.01, label="Tolerance (m)")
                speed = gr.Slider(0.10, 2.00, value=0.5, step=0.05, label="Speed (m/s)")
                kp = gr.Slider(0.50, 20.0, value=5.0, step=0.5, label="Heading gain Kp")
                rounds = gr.Slider(1, 6, value=3, step=1, label="Tuning rounds")
                model_id = gr.Textbox(value="nvidia/nemotron-3-super-120b-a12b",
                                      label="Model id")
                use_mock = gr.Checkbox(value=False,
                                       label="Mock mode (no API calls)")
                go = gr.Button("Run", variant="primary")
            with gr.Column():
                out = gr.Image(label="Simulation", type="numpy", height=520)
                log = gr.Textbox(label="The model's reasoning, round by round",
                                 lines=20, max_lines=40)

        go.click(run_task,
                 inputs=[start_r, start_c, goal_r, goal_c, tol, speed, kp,
                         rounds, model_id, use_mock],
                 outputs=[out, log])

    return demo


if __name__ == "__main__":
    build_ui().launch()
