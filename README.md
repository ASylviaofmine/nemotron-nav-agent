# nemotron-nav-agent

**A wheeled robot that plans with A\* and tracks with a proportional controller — supervised by an NVIDIA Nemotron model running on Nebius Token Factory.**

The model does not drive the robot. It reads the measured tracking error and
proposes the next parameter change; the simulator re-runs and keeps the change
only if the numbers actually improved.

```
natural-language task
        │
        ▼
   plan_task()          Nemotron → {start, goal, tol, speed, Kp}
        │
        ▼
   plan → drive → measure
                   max/mean cross-track error, end-point error, time
        │
        ▼
   diagnose()           Nemotron → a diagnosis + proposed parameter changes
        │
        ▼
   re-run with the new parameters
        │
        ▼
   keep the change only if the measured numbers improved
```

Built for the [Nebius Global AI Hackathon](https://nebiusglobalaihackathon.devpost.com)
(Physical AI track). The inference calls in this project run on **Nebius
Token Factory** against an **NVIDIA Nemotron** model, as the rules require.

---

## Why this project is not a chatbot in front of a simulator

Judges for this kind of track have seen a hundred "LLM + simulation" projects
where the language model is decoration. Three things here are designed to make
that impossible to hide:

**1. The model supervises; it never steers.** A\* still plans the route and
the controller still drives the robot. The model chooses *parameters* and
decides *which error to fix next*. It is never asked to invent robot physics
or output motor commands, because a language model that cannot be checked
against a measurement is a language model that cannot be evaluated.

**2. Every suggestion is falsifiable.** A proposed change is clamped to a
legal range, applied, and the simulation is re-run. The measured before/after
numbers decide whether it was kept. "The model said it would help" is never
the claim — the table is.

**3. There is a no-model control row.** The model's system prompt spells out
the tuning knowledge that was measured on this simulator. That same knowledge
is also applied as a **fixed rule with no model involved** (`Kp = 12`). If the
agent cannot beat that control, the model is decoration — and the evaluation
table says so, in a row anyone can read. This is the row that makes the
other rows mean something.

On top of that, the whole thing is checked against an **exhaustive sweep of
125 parameter combinations** that involves no model at all. That sweep is
deterministic, lives in this repository, and can be re-run by anyone — so
"the agent got within X of the best of 125 combinations" is a checkable
statement rather than a claim.

---

## The metric, and why it is the hard part

Everything here hinges on one definition, and getting it wrong would have
hidden the entire effect of every parameter.

**Cross-track error is the distance from the trajectory to the planned
polyline — not the distance to the nearest waypoint.**

With waypoints one metre apart, a robot that tracks the path *perfectly* is
still up to 0.5 m from the nearest waypoint, roughly half the time. The
wrong definition therefore produces a constant that looks like the grid
spacing and swamps the signal. On the same trajectory:

| metric | mean | max |
|---|---|---|
| distance to nearest waypoint (**wrong**) | 0.251 m | 0.493 m |
| distance to the polyline (**used here**) | 0.0126 m | 0.0895 m |

`tools/selftest.py` asserts both facts: that the wrong metric is non-zero on
a path-following trajectory, and that the vectorised implementation is
bit-for-bit identical to a naive per-point loop (max abs diff `0.00e+00`).

---

## Results

### The canonical map

| Reference | Max cross-track (m) | Time (s) | Parameters |
|---|---|---|---|
| Fixed baseline | 0.0895 | 32.00 | tol=0.05, speed=0.5, Kp=5.0 |
| Prior-knowledge control (no model) | 0.0233 | 31.75 | tol=0.05, speed=0.5, Kp=12.0 |
| Exhaustive best of 125 | 0.0143 | 53.20 | tol=0.02, speed=0.3, Kp=12.0 |

### Generalisation over 10 maps

The same loop, over a deterministic suite of maps: the canonical wall map, a
wall map with the openings moved, and 8 random obstacle maps (seeded, and
filtered to keep only solvable ones).

| Metric | Value |
|---|---|
| Maps evaluated | 10 |
| Improved over baseline | 10 |
| Regressed | 0 |
| Median baseline cross-track | 0.0687 m |
| Median agent cross-track | 0.0255 m |
| Median improvement | 62.9 % |
| Worst-case improvement ratio | 2.08× |

Reproduce with `python tools/agent_eval.py`.

> **A note on honesty about these numbers.** The tables above were produced
> with the offline mock (`--mock`), where the *pipeline and every measured
> quantity are real* but the *suggestions come from a fixed rule*. That
> makes the agent rows **identical to the no-model control by
> construction** — which is exactly why the control row exists. The live
> numbers, with Nemotron generating the suggestions, are produced by the same
> script without `--mock` once a `NEBIUS_API_KEY` is present. The
> deterministic reference numbers (fixed baseline, exhaustive sweep, all
> metrics) do not depend on the model and are reproducible offline today.

---

## Running it

```bash
git clone <this-repo>
cd nemotron-nav-agent
pip install numpy pillow          # the core needs nothing else
```

### In PyCharm

Open the folder `nemotron-nav-agent` (**File → Open**, pick the directory
itself, not the parent). The project ships with six run configurations in
`.run/`, so they appear in the run dropdown straight away:

| Configuration | What it does |
|---|---|
| `run: plan + track` | `main.py run` — plan, track, print the metrics |
| `run: record demo GIF` | `main.py run --gif` — write `docs/demo.gif` |
| `tune: let the model tune the tracker` | `main.py tune` — the supervision loop |
| `evaluate: the full evaluation` | `main.py evaluate` — the three tables |
| `selftest` | `tools/selftest.py` — all the checks |
| `demo: Gradio web app` | `app.py` — the web demo |

The interpreter is a virtualenv in the project folder, created with
`--system-site-packages` so numpy, Pillow and gradio are already there
without a network install. If you open the project on a different machine,
point the interpreter at any Python 3.11+ that has numpy and Pillow.

> pygame is **not** required. It is used only by the interactive window in
> `src/viewer.py`. The GIF recorder and the web demo share the numpy
> renderer in `src/render.py`, so the video works with numpy and Pillow
> alone.

### The four commands

```bash
python main.py run                 # plan + track, print the metrics
python main.py run --gif           # ... and record docs/demo.gif
python main.py tune                # let the model tune the tracker
python main.py evaluate            # the full evaluation, three tables
python main.py evaluate --mock     # ... without calling the API
```

### With a live model

```bash
export NEBIUS_API_KEY=nb-...
export NEBIUS_MODEL=nvidia/nemotron-3-super-120b-a12b   # optional
python main.py tune
python tools/agent_eval.py
```

Which models are available right now:

```bash
python -m src.nebius_client --list-models
```

### The web demo

```bash
pip install gradio
python app.py
```

The demo shows the simulation and the model's reasoning side by side, updated
round by round, with the measured before/after numbers next to each
suggestion. That pairing is the whole point of the project: the model
proposes, the simulator disposes, and you can watch both halves of the
exchange.

### The self-test

```bash
python tools/selftest.py
```

Checks that `src/metrics.py` and the independent implementation in
`tools/benchmark_ref.py` agree bit for bit; that the cross-track definition
is the right one; that the vectorised and naive implementations are
identical; that two identical runs produce identical numbers; that the agent
loop produces valid metrics; and that every map in the suite is solvable.

---

## Layout

```
main.py                  CLI: run / tune / evaluate
app.py                   Gradio demo
src/
  grid.py                occupancy grid, cell <-> world coordinates
  planner.py             A* (4-connected, Manhattan heuristic, admissible)
  controller.py          go-to-goal proportional control, angle wrapping
  simulation.py          map -> plan -> track, packaged as one "run"
  metrics.py             cross-track, end-point error, distance, time
  render.py              numpy framebuffer (GIF + demo, no pygame needed)
  viewer.py              interactive pygame window (optional)
  nebius_client.py       Token Factory client (stdlib urllib, zero deps)
  agent.py               the Nemotron supervision layer
  benchmark.py           multi-map evaluation suite
tools/
  selftest.py            the self-test
  agent_eval.py          the evaluation, three tables
  benchmark_ref.py       independent metric implementation, for cross-checking
```

---

## The pieces worth reading

### A\* with a heuristic that is actually admissible

4-connected grid, unit step cost, Manhattan heuristic. The robot can only
move up, down, left or right and each step costs exactly 1 — diagonals do
not exist — so the Manhattan distance is precisely "how many steps remain in
the best case without hitting a wall". It never overestimates, so A\* returns
a shortest path. Out-of-bounds counts as wall, which keeps the neighbour
check down to one line.

### The controller, and the one bug worth remembering

Proportional go-to-goal steering, `theta += Kp * e * dt`, with the heading
error wrapped into `(-π, π]`. Without the wrap, `theta` accumulates into the
tens of radians, the error explodes with it, and the robot spins on the spot
without ever converging on its target. This is a two-line fix and it is the
difference between a robot and a top.

### The measurement reaches the model as prose, not as a table

Metrics are handed to the model as sentences — "max cross-track error:
0.0895 m" — because the magnitude relationships carry over better than a
markdown table does. Numbers keep their full precision; they are not rounded
into integers on the way in.

### The model's suggestion is clamped, and the clamp is visible

`tol ∈ [0.01, 0.50]`, `speed ∈ [0.10, 2.00]`, `Kp ∈ [0.50, 20.0]`. A
suggestion like "Kp = 500" is clamped before it is used, because a
parameter outside the range produces a run that means nothing.

### The comparison that is lexicographic, and why

Cross-track error is compared first and time second, because the point of
this project is *"the robot follows the path it was given"*, not *"the robot
arrives quickly"*. The measurements agree: speed buys time with fidelity,
linearly.

---

## Cost

`nvidia/nemotron-3-super-120b-a12b` on Token Factory is $0.30 / $0.90 per
1M input / output tokens; the 30B Nano is $0.06 / $0.24. The full
evaluation makes roughly 30 short calls, so it costs **a fraction of a
cent** — the expensive part of this project was writing it, not running it.

The client is written against the standard library (`urllib`) on purpose: one
less package that can fail to install is one less risk nine days before a
deadline. It also retries with a different model ID on a 400 or 404, because
the Nemotron model IDs are spelled inconsistently across the platform's own
pages.

---

## Reproducibility

- The map suite is seeded (`seed=42`); the same ten maps every time.
- The simulator is deterministic; two identical runs produce identical
  numbers, and the self-test asserts it.
- The exhaustive sweep is 125 fixed combinations, checked into the
  repository, and involves no model.
- Every number in this README is regenerated by one script:
  `python tools/agent_eval.py`.

## License

MIT — see `LICENSE`.
