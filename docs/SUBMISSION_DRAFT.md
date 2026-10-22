# Devpost submission — draft text

Everything below is what the submission form asks for. Fill it in as-is;
the code already exists and the numbers are the ones the scripts print.

---

## Team

`ASylviaofmine` (solo). If you would rather submit as a team, add the
members here before submitting — a team submission needs a designated
Representative, and only the Representative can press the button.

---

## Project title

**nemotron-nav-agent**

---

## Project description (the long text)

A wheeled robot that plans with A\* and tracks with a proportional
controller — supervised by an NVIDIA Nemotron model running on Nebius
Token Factory.

The model does not drive the robot. It reads the measured tracking error
and proposes the next parameter change; the simulator re-runs and keeps the
change only if the numbers actually improved.

**The problem this addresses.** A controller has parameters, and the
right values depend on the map, the speed and the accuracy you care about.
Tuning them by hand means running a sweep, reading a table, and guessing
which knob to turn next. That loop is exactly the kind of thing a language
model is good at *framing* — and exactly the kind of thing that goes wrong
when a language model is allowed to assert results instead of proposing
changes that must then be verified.

**The approach.** The model reads the measured error of the last run
(max cross-track error, mean cross-track error, end-point error, time) and
answers with a diagnosis and a proposed parameter change. The change is
clamped to a legal range, applied, and the simulation is re-run. The
measured numbers decide whether it was kept. A* still plans the route and
the controller still drives the robot; the model chooses *parameters* and
decides *which error to fix next*. It is never asked to invent robot
physics or output motor commands.

**Why the model is not decoration.** Three things make that checkable
rather than a claim:

1. *A no-model control row.* The tuning knowledge the model's system
   prompt spells out is also applied as a fixed rule with no model
   involved. If the agent cannot beat that, the model is decoration — and
   the evaluation table says so, in a row anyone can read.
2. *An independent exhaustive reference.* The best of all 125 swept
   parameter combinations is computed by a deterministic script that
   involves no model at all, so "the agent reached within X of the best of
   125" is a statement a reviewer can verify by running one file.
3. *The metric is defined, tested and honest.* Cross-track error is
   measured to the planned polyline, not to the nearest waypoint. The
   wrong definition produces a constant that looks like the grid spacing
   and hides the effect of every parameter; the self-test asserts that the
   right one is used and that the vectorised implementation is bit-for-bit
   identical to a naive loop.

**The results.** On the canonical map, max cross-track error falls from
0.0895 m to 0.0233 m — a 3.8× reduction — while the time to goal
*improves* slightly (32.00 s → 31.75 s). The agent lands within 0.0090 m
of the best of all 125 swept combinations, and on 10 of 10 maps in a
seeded suite it improves on the baseline, with a worst-case improvement
ratio of 2.08×.

**What it is built on.** Python, numpy, and a Token Factory client written
against the standard library (`urllib`) on purpose — one less package that
can fail to install is one less risk. The project also runs offline: with
no API key the whole pipeline still executes, and only the suggestions
come from fixed rules, so the system can be reviewed before an account
exists.

---

## Links

| Field | Value |
|---|---|
| Repository | `https://github.com/ASylviaofmine/nemotron-nav-agent` |
| Demo URL | *not required for the Physical AI track* — leave blank |
| Video | *your YouTube link* |

---

## Track

**Physical AI.**

---

## What you used — Nebius and NVIDIA feedback

This is a required field. Say what you actually used, honestly — including
what was hard. Draft:

> **Token Factory.** Used the OpenAI-compatible Chat Completions endpoint at
> `api.tokenfactory.nebius.com/v1` with NVIDIA Nemotron models. The model
> IDs are spelled inconsistently across Nebius's own documentation pages
> (`nvidia/nemotron-3-super-120b-a12b` vs
> `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B` vs `nvidia/Nemotron-3.5-Super-VL`),
> so the client queries `/models` at runtime and falls back through a list
> of candidates on a 400 or 404. That fallback is the first thing I would
> change if I were starting over — it cost more debugging time than the
> rest of the client put together.
>
> The model was genuinely useful for one thing: framing the diagnosis.
> "Cross-track error dominates the residual; the heading gain is too low
> for the requested speed" is a better starting point for a parameter
> search than the raw metric list, and it is the part I would keep.
>
> What I would not claim: that the model beat a well-written heuristic.
> That is why the evaluation reports a no-model control row. On this
> simulator the tuning knowledge is simple enough that a fixed rule gets
> most of the way, and the honest result is that the model's contribution
> is the *diagnosis and the search direction*, not a large final margin.
> The framework would earn its keep on a controller with more interacting
> parameters than this one has.
>
> **AI Cloud.** Not used. The Physical AI track does not require it, and
> the project's requirement is satisfied by the runtime Token Factory call
> rather than by deployment. Serverless Jobs would be the right tool for
> running the parameter sweep across many maps in parallel, which is the
> obvious next step if the map suite grows.
>
> **NVIDIA models.** Nemotron 3 (Super 120B-A12B, and Nano 30B-A3B as the
> cheaper option). The token cost of a full evaluation run is a fraction
> of a cent, which made it cheap to iterate on the prompt and the
> evaluation protocol.

---

## Before you submit — checklist

- [ ] Repository is **public**, has the **MIT license** file, and the
      README is the first thing on the landing page.
- [ ] The repository description on the GitHub page is set, and the
      topics include `nvidia`, `nebius`, `nemotron`, `robotics`, `physical-ai`.
- [ ] `python tools/selftest.py` passes on a fresh clone.
- [ ] `python tools/agent_eval.py` reproduces the numbers in the README.
- [ ] The YouTube video is **publicly visible** (not unlisted) and under
      3 minutes, with at least 1 minute showing the modules in action.
- [ ] The video link is in the README as well as on the form.
- [ ] The model ID and the token spend are mentioned in the README.
- [ ] Everything is in English (the video included — add subtitles if you
      narrate in Chinese).
- [ ] Press **Submit** before **30 Oct 2026, 10:00 PDT**.
