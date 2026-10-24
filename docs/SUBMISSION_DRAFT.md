# Devpost submission — draft text

Everything below is what the submission form asks for. Fill it in as-is;
the code already exists and the numbers are the ones the scripts print.

---

# ⬇️ 复制粘贴区 ⬇️

> **这一整块就是表单要填的内容。** 灰色背景的框 = 直接复制。
> 框下面的说明文字是给你看的，**不要复制**。

## 字段 1 — Project name

```
nemotron-nav-agent
```

## 字段 2 — Elevator pitch

```
A* plans the route, a proportional controller tracks it, and an NVIDIA Nemotron model on Nebius Token Factory supervises the controller's parameters, each change verified by re-running.
```

## 字段 3 — Thumbnail image

**上传文件**（不是粘贴文字）：`docs/thumbnail.png`

## 字段 4 — Team

```
ASylviaofmine
```

# ⬆️ 复制粘贴区结束 ⬆️

---

# ⬇️ Project details 页（第二页）复制粘贴区 ⬇️

## 字段 5 — About the project（Project Story）

**完整的 Project Story 在 `docs/PROJECT_STORY.md`** —— 打开那个文件，
全选（Ctrl+A）、复制（Ctrl+C），粘贴到这里。

它已经按 Devpost 给的模板分好节了：

```
## Inspiration
## What it does
## How we built it
## Challenges we ran into
## Accomplishments that we're proud of
## What we learned
## What's next for nemotron-nav-agent
```

粘贴后删掉模板里那些空的占位行（如果还有残留的 `##` 标题）。

## 字段 6 — Built with（最多 25 个）

逐个添加，**23 个**：

```
Python
NumPy
Pillow
OpenCV
Gradio
NVIDIA Nemotron
Nemotron 3 Super 120B
Nebius Token Factory
A* pathfinding
Path planning
Control theory
Proportional control
Robotics
Robotics simulation
Artificial Intelligence
LLM
Agent
Evaluation
Benchmarking
Physical AI
Simulation
Automation
```

> 标签是评委和搜索系统看的关键词，所以把 "NVIDIA Nemotron"、
> "Nebius Token Factory"、"Physical AI" 这些**精确的名字**写进去。
> 别写没用到的技术（这个项目没用强化学习，也没用梯度下降）。

## 字段 7 — Try it out links（必填）

**第一个链接**（仓库）：

```
https://github.com/ASylviaofmine/nemotron-nav-agent
```

**第二个链接**（点 "ADD ANOTHER LINK"，视频）：

```
https://github.com/ASylviaofmine/nemotron-nav-agent/blob/master/docs/submission.mp4
```

> 规则里写了 demo URL 对 Physical AI **不要求**，但这个字段标着必填，
> 所以至少填一条。仓库链接是最诚实的选择——它就是评委要"try it out"的东西。
> 视频链接放第二条，因为它是这个项目**唯一能在浏览器里直接看**的东西。

## 字段 8 — Image gallery（最多 15 张，5 MB 上限，3:2 比例）

上传这 5 张（都已裁成 3:2，1000×666）：

| 文件 | 内容 |
|---|---|
| `docs/gallery_title.png` | 标题卡 |
| `docs/gallery_supervise.png` | **基线 vs 调优 + 实时误差曲线** ← 最重要 |
| `docs/gallery_generalise.png` | 10 图套件条形图 |
| `docs/gallery_decide.png` | 模型诊断 + 为什么停手 |
| `docs/gallery_conclusion.png` | 结论表 + 穷举参照系 |

**上传顺序很重要**：把 `gallery_supervise.png` 放**第一张**——
它是唯一一张不用解释就能看懂"模型做了什么"的图。

## 字段 9 — Demo video URL（必填）

```
（你的 YouTube 链接）
```

- 只能是 **YouTube 或 Vimeo**
- **可见性设为 public 或 unlisted，不能设成 private**
- 只有**前 3 分钟**会被看（你的视频 81 秒，全部都在前 3 分钟里）
- Physical AI 要求**至少 1 分钟**展示关键模块动作 ← 81 秒达标

# ⬆️ Project details 复制粘贴区结束 ⬆️

---

## 字段说明（不用复制）

### Project name
60 字符上限，这个才 19 个。

### Elevator pitch
200 字符上限，这个是 185 个。

一句话说了三件事：**经典栈**（A\* + 比例控制）、**模型**（Nemotron on
Token Factory 负责监督参数）、**验证**（每次改动都要重跑确认）。
最后半句 "each change verified by re-running" 是整个项目的核心论点，
不能丢。

> 备选（182 字符，更平铺直叙一些）：
>
> `A wheeled robot plans with A* and tracks with a proportional controller. An NVIDIA Nemotron model on Nebius Token Factory reads the measured error and proposes each parameter change.`
>
> 两个都合格。上面那个更好——它多说了"验证"。

### Thumbnail image
视频里最有说服力的那一帧：基线和调优后并排，各自带一条实时误差曲线。
它不用一个词就说清了"0.0895 m versus 0.0233 m"——这正是缩略图该干的事。

*(PNG 格式，1000×700，约 100 KB，远低于任何上传限制。)*

---

## Page 2 — Project details

### Team

`ASylviaofmine`（个人参赛）。如果想组队，现在就加——团队提交需要指定
Representative，而且只有 Representative 能按提交按钮。

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

**Why this pattern is worth building.** Robot tuning is a search problem
wearing a costume: today it is done by sweeping parameters, reading a
table, and guessing which knob to turn next. The simulation is the cheap
part; choosing the next candidate is the step that needs judgement. A model
that has seen the measured error can name the dominant error source and
propose the next candidate, and the simulator answers the only question
that matters.

The same loop against real hardware costs a physical trial per candidate,
and there the value of the model is not "it found Kp = 12" but "it did not
waste the next twenty trials on a parameter that was never going to help".
The verification step does not change; only its cost does.

I am deliberately not claiming the model beats a well-written heuristic —
on this simulator the tuning knowledge is simple enough that a fixed rule
gets most of the way, and the evaluation reports that control row so the
distinction is visible rather than implied. The claim is narrower and
defensible: **the model produces a useful diagnosis, and the framework
keeps only the changes that measurably worked.** The interesting version
is not more parameters but more *systems* — each additional controller,
sensor model or failure mode adds error sources the engineer has not
enumerated, which is exactly when "here are the metrics, what should I
try next?" is worth more than a fixed table of prior experience.

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

> **This field is a judged prize on its own.** The hackathon lists
> *"Most Valuable Feedback — $100 cash, 10 winners, NVIDIA swag pack"*, and
> the rules say feedback entries are scored on **completeness, viability and
> potential impact**. So this is not a box to tick. Write it as a standalone
> piece of useful feedback that would help another builder — specific,
> actionable, and honest about where the tools did and did not help.
> That is also the version most likely to win the main prizes, because the
> reviewers of this project are the same people who wrote the docs.

Paste the draft below.

---

> **Token Factory — what worked**
>
> The OpenAI-compatible endpoint at `api.tokenfactory.nebius.com/v1` was
> straightforward to integrate: standard `/chat/completions`, standard
> bearer auth, and it accepted the same client code I already use for
> OpenAI-compatible endpoints. My client is written against `urllib` from
> the standard library, so the project has one less dependency that can
> fail to install — which mattered more to me than it might sound, since I
> wanted the repository to be reviewable before anyone had an account.
>
> The thing that made it genuinely useful was **not** the model being
> clever. It was the model turning a metric dump into a sentence. My
> agent hands it "max cross-track 0.0895 m, mean 0.0126 m, time 32.00 s"
> and gets back *"cross-track error dominates the residual; the heading gain
> is too low for the requested speed."* That is a **search direction**, not
> a number, and it is the part I would keep even if the underlying model
> were swapped tomorrow.
>
> **Token Factory — what I would fix**
>
> The model IDs are spelled inconsistently across Nebius's own pages. I
> found at least three spellings in circulation:
> `nvidia/nemotron-3-super-120b-a12b`,
> `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, and
> `nvidia/Nemotron-3.5-Super-VL`. The first one is not the one that
> appears in the quickstart. A builder following the documentation in
> order can end up with a 404 on their first call and no obvious way to
> tell whether the problem is their code or the ID. My client now queries
> `/models` at runtime and falls back through a candidate list on a 400 or
> 404, but a canonical list — or a documented alias — would save everyone
> that work. **Concrete suggestion: publish the exact IDs that
> `/v1/models` returns for the Nemotron family in the quickstart, and
> state whether the canonical form is the `nvidia/`-prefixed one.**
>
> Two smaller things. First, the `list-models` response is the only
> reliable source of truth, and it is not mentioned in the quickstart —
> worth one line. Second, there is no way to pin "the cheapest model that
> can do this", so a builder comparing Super and Nano has to work it out
> from the pricing table. A "recommended for cheap classification" note
> per model would help.
>
> **What I would not claim.** The model did not beat a well-written
> heuristic on this simulator, and my evaluation says so in a row anyone
> can read. The tuning knowledge here is simple enough that a fixed rule
> gets most of the way. The model's contribution is the **diagnosis and
> the search direction**, not a large final margin. I would rather state
> that plainly than have a judge find it — and on this project the
> interesting version is not more parameters but more *systems*, where the
> error sources have not been enumerated in advance.
>
> **AI Cloud — not used, and why that is a deliberate choice**
>
> The Physical AI track does not require deployment, and the project's
> requirement is satisfied by the runtime Token Factory call rather than
> by hosting. Deployment would have added a moving part without adding
> evidence. Where it *would* earn its place is **Serverless Jobs**: the
> parameter sweep across many maps is embarrassingly parallel, and running
> the 125-combination sweep plus the 10-map generalisation suite as
> background jobs would let the evaluation scale to hundreds of maps
> without changing the code that does the measuring. That is the concrete
> next step I would take, and it is why I mention Jobs specifically rather
> than saying "I would use AI Cloud".
>
> **NVIDIA models**
>
> Nemotron 3 — Super 120B-A12B, with Nano 30B-A3B as the cheaper option
> worth reaching for when the task is only "name the dominant error
> source". A full evaluation run costs **a fraction of a cent**, which
> made it cheap enough to iterate on the prompt and on the evaluation
> protocol itself. That cheapness was the enabling condition for this
> project: I could re-run the whole thing dozens of times while deciding
> what "better" should even mean, and the measurement discipline in the
> repository came out of that.
>
> **One thing I would want to know from other builders.** Has anyone found
> a reliable way to make Nemotron output a strictly-typed parameter
> proposal that can be validated against a schema? I used a
> JSON-structured request plus clamping on my side, which works, but a
> schema-enforced mode would remove a whole class of failure from the
> "LLM in the loop" pattern.

---

## Appendix: the prizes this project is aiming at

Listed on the hackathon page, in case it changes how the fields are
weighted:

| Prize | Amount | Relevance |
|---|---|---|
| Grand Prize | $20,000 | main award, four equal criteria |
| Physical AI Track Winner | $20,000 + **NVIDIA Jetson Orin Nano** | this is the target track |
| Most Valuable Feedback | **$100 × 10** + NVIDIA swag | **the feedback field, judged separately** |
| City Winner Awards | $500 × 20 | only if you attended a Builders & Brews event |

The feedback field being its own prize category is the reason the draft
above is long and specific. A two-line "it worked fine" would be a wasted
opportunity.

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
