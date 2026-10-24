## Inspiration

Robot controllers are tuned by hand: you sweep a few parameter values, read a table of errors, and guess which knob to turn next. The simulation is the cheap part. **Choosing the next candidate is the step that needs judgement** — and that judgement is exactly what a language model is good at framing, provided it is never allowed to assert the result.

The rule this project follows is simple, and it is the whole design:

> **The model proposes. The simulator disposes. The measurement decides.**

No sentence a model writes is ever taken as a result. Every suggestion is clamped to a legal range, applied, and the simulation is re-run. If the measured numbers did not improve, the change is discarded and the model is told so.

## What it does

A wheeled robot plans a route with **A\*** on a 4-connected grid and tracks it with a **go-to-goal proportional controller**. An **NVIDIA Nemotron** model running on **Nebius Token Factory** supervises the controller's parameters.

```
natural-language task
        |
        v
   plan_task()          Nemotron -> {start, goal, tol, speed, Kp}
        |
        v
   plan -> drive -> measure
                   max/mean cross-track error, end-point error, time
        |
        v
   diagnose()           Nemotron -> a diagnosis + proposed parameter changes
        |
        v
   re-run with the new parameters
        |
        v
   keep the change only if the measured numbers improved
```

The model **never plans a route and never drives the robot**. It chooses parameters and decides which error to fix next — never motor commands, never invented physics. A language model that cannot be checked against a measurement is a language model that cannot be evaluated, so this one is never asked for anything that cannot be measured.

**Results on the canonical map:**

| Reference | Max cross-track | Time | Parameters |
|---|---|---|---|
| Fixed baseline | 0.0895 m | 32.00 s | tol=0.05, speed=0.5, Kp=5.0 |
| After Nemotron | **0.0233 m** | **31.75 s** | tol=0.05, speed=0.5, Kp=12.0 |
| Exhaustive best of 125 | 0.0143 m | 53.20 s | tol=0.02, speed=0.3, Kp=12.0 |

A **3.8x** reduction in tracking error, *and* slightly faster — better tracking bought with no time cost. Across a seeded suite of 10 maps the agent improves on **all 10** (median 62.9% lower error, worst-case ratio 2.08x).

## How we built it

**The classical half** is written from scratch, no learning and no model calls:

- **A\*** on a 4-connected grid with a Manhattan heuristic. The robot can only move up, down, left or right and every step costs exactly 1, so the Manhattan distance is precisely the number of steps remaining in the best case — the heuristic never overestimates, and A\* returns a shortest path. Out-of-bounds counts as wall, which keeps the neighbour check down to one line.
- **A proportional go-to-goal controller**, `theta += Kp * e * dt`, with the heading error wrapped into `(-pi, pi]`. Without that wrap `theta` accumulates into the tens of radians, the error explodes with it, and the robot spins on the spot without ever converging. That two-line fix is the difference between a robot and a top.
- **Cross-track error measured to the planned polyline**, not to the nearest waypoint. Waypoints sit 1 m apart, so a robot tracking the path *perfectly* is still up to 0.5 m from the nearest waypoint, roughly half the time. The wrong definition returns a near-constant that looks like half a grid cell and hides the effect of every parameter. On the same trajectory the wrong metric reads 0.251 m mean where the right one reads 0.0126 m.

**The supervision half** is an OpenAI-compatible client against `api.tokenfactory.nebius.com/v1`, written against the standard library (`urllib`) so the project has one less dependency that can fail to install — which mattered, because the repository should be reviewable before anyone has an account.

**Three things make the evaluation checkable rather than a claim:**

1. **A no-model control row.** The tuning knowledge the model's system prompt spells out is also applied as a fixed rule with no model involved. If the agent cannot beat that, the model is decoration — and the table says so, in a row anyone can read.
2. **An independent exhaustive reference.** The best of all 125 swept parameter combinations is computed by a deterministic script involving no model at all, so "the agent landed within 0.0090 m of the best of 125" is a statement a reviewer can verify by running one file.
3. **The metric is tested.** `tools/selftest.py` asserts that the vectorised implementation in `src/metrics.py` is bit-for-bit identical to the naive per-point loop in `tools/benchmark_ref.py` (max abs diff `0.00e+00`), that the wrong metric is non-zero on a path-following trajectory, and that two identical runs produce identical numbers.

**Everything runs offline.** With no API key the whole pipeline still executes and every measured quantity is real — only the suggestions come from fixed rules. The project can be reviewed before an account exists.

## Challenges we ran into

**The metric nearly hid the entire effect.** The first version measured cross-track error to the nearest waypoint, which returns a number around 0.25 m no matter what the controller does. Every parameter looked equally bad. Fixing the definition was the single change that turned an unmeasurable project into a measurable one.

**`theta` grew without bound.** Without angle wrapping the heading error kept growing instead of shrinking, and the robot circled. The symptom looked like "the controller does not work" rather than "the error term needs wrapping".

**The model IDs are spelled inconsistently across Nebius's own documentation pages.** At least three spellings are in circulation (`nvidia/nemotron-3-super-120b-a12b`, `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, `nvidia/Nemotron-3.5-Super-VL`), and the first one is not the one in the quickstart. The client now queries `/models` at runtime and falls back through a candidate list on a 400 or 404.

**A label that lied.** The video's error plot was labelled "max cross-track" but printed the instantaneous value. The robot passes exactly over the planned line at moments, so the panel regularly displayed `max cross-track 0.0000 m` next to a curve that visibly oscillated — a number nobody checked, on the frame the video lingers on. It now prints the running maximum.

**Renderers drift.** The GIF recorder and the web demo originally had separate drawing code, so the video and the demo could disagree. Both now share one numpy framebuffer in `src/render.py`.

## Accomplishments that we're proud of

**The evaluation has an honest negative result in it.** The model did **not** beat a well-written heuristic on this simulator — the tuning knowledge is simple enough that a fixed rule gets most of the way. Rather than hide that, the evaluation reports it as a row anyone can read, and the claim becomes narrower and defensible: *the model produces a useful diagnosis, and the framework keeps only the changes that measurably worked.* A judge can verify the limitation instead of discovering it.

**The pattern does not depend on the model.** Swapping the LLM changes how good the diagnosis is, not whether a proposal is accepted. That is what makes the loop usable on hardware, where a wrong suggestion costs a physical trial rather than a millisecond.

**The whole thing is reproducible offline in one file.** `python tools/selftest.py` and `python tools/agent_eval.py` regenerate every number in this project. The evaluation suite is seeded, the simulator is deterministic, and the exhaustive sweep is checked in.

**A full evaluation costs a fraction of a cent.** Nemotron 3 Super at $0.30/$0.90 per 1M input/output tokens and roughly 30 short calls made it cheap to iterate on the prompt and on the evaluation protocol. That cheapness was the enabling condition for the whole project.

## What we learned

**The verification step is the product.** The interesting part was never "call an LLM". It was building a loop where a suggestion can be *wrong* without costing anything, so that the model's judgement can be separated from its arithmetic. Adding the re-run-and-compare step made every other design choice easier.

**A metric can quietly destroy a project.** Both the wrong cross-track definition and the mismatched video label produced numbers that looked plausible and meant nothing. Neither was caught by the code; both were caught by reading the output.

**An LLM is good at naming an error, not at fixing one.** "Cross-track error dominates the residual; the heading gain is too low for the requested speed" is a *search direction*, and it was the part worth keeping. The final numbers came from the simulator, not the model.

**Write the control experiment first.** The no-model control row was added after the first results looked good — and it immediately reframed the claim. Having it in the table from the start would have saved the reframe.

**Honesty is a competitive advantage, not a liability.** A judge who finds a limitation you did not mention concludes the whole project is unexamined. A judge who finds one you flagged concludes the rest of it can be trusted.

## What's next for nemotron-nav-agent

**More systems, not more parameters.** The framework is deliberately narrow: three parameters, one map family. The interesting version is the opposite of "add more knobs" — each additional controller, sensor model or failure mode adds error sources the engineer has not enumerated, which is exactly when "here are the metrics, what should I try next?" is worth more than a fixed table of prior experience. The `run_tuning(evaluate=...)` seam in `src/agent.py` exists for that: the loop does not know what it is tuning, only how to propose and how to verify.

**Deploy the sweep on Nebius Serverless Jobs.** The parameter sweep across many maps is embarrassingly parallel. Running the 125-combination sweep and the generalisation suite as background jobs would let the evaluation scale to hundreds of maps without changing the code that does the measuring.

**Move it onto hardware.** The simulator makes a wrong suggestion cost milliseconds. On a real robot the same loop costs a physical trial, and the value of the model is no longer the parameter it found but the trials it did not waste.

**Take the lesson past robotics.** "The model proposes, the physical system disposes, the measurement decides" is a pattern that applies wherever a learned controller is tuned against a slow, expensive, measurable reality — and it is the shape that makes the LLM-in-the-loop pattern safe rather than decorative.

---

*Repository: public, MIT licensed, and runnable offline with only `numpy` and `Pillow`. Every number above is regenerated by a script in the repository.*
