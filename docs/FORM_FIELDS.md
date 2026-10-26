# Additional info 页 + 反馈字段 — 逐字段答案

> **这一页是给评委和主办方看的，不会出现在你的公开项目页上。**
> 但那几个反馈字段是 **"Most Valuable Feedback" 独立评奖项**（$100 × 10 名）
> 的评奖内容 —— 规则原文：按 **completeness、viability、potential impact** 评估。
> 所以别敷衍，写得越具体越有希望。

## 哪些字段写短的，哪些写长的

| 字段 | 用哪版 | 为什么 |
|---|---|---|
| 9. Demo URL | 留空 | 规则明说 Physical AI 不要求 |
| **10. Which model(s)** | **短版（719 字符）** | 提示写着 "e.g., Nemotron-4 340B, Nemotron-Mini"——问的是事实，不是论述 |
| 11. 输出质量评分 | 长版 | **反馈评奖内容** |
| 12. fine-tune / prompt 工程 | 长版 | **反馈评奖内容** |
| 13. 与其他模型对比 | 长版 | **反馈评奖内容** |
| 14. 哪些 Nebius 能力最有用 | 长版 | **反馈评奖内容** |
| 15. 推荐意愿评分 | 长版 | **反馈评奖内容** |
| 16. 相比其他云的体验 | 长版 | **反馈评奖内容** |
| 17. 想要什么改进 | 长版 | **反馈评奖内容** |
| 18. 希望看到什么 | 长版 | **反馈评奖内容** |
| 22. 用了哪些 AI 工具 | 中等 | 如实写，但别喧宾夺主 |
| 其它（1-8、19-21、23-24） | 都很短 | 一两行的事 |

**判断标准很简单**：字段提示里带 "e.g., ..." 的是事实题，短的；
带 "Please share..." / "What worked well or fell short" 的是论述题，写长的。

---

# ⬇️ 复制粘贴区 ⬇️

## 1. Upload a File

## 1. Upload a File

**上传这个文件**（不是必填，但值得上传）：

```
C:\Users\Lee\WorkBuddy\2026-10-21-22-18-37\nemotron-nav-agent\docs\nemotron-nav-agent-submission.zip
```

13.4 MB（限制 35 MB），48 个文件。**这是整个仓库的快照**，
评委解压后 `pip install numpy && python tools/selftest.py` 就能跑，
**不用 clone、不用进 GitHub**。

已实测：解压到临时目录后自检通过，两个视频都在里面。

> 为什么要传：规则里有一条"Judges are not required to test the Project"，
> 但如果评委真的想跑，有个 zip 会省掉他注册账号和配环境的步骤。
> **5 秒钟的事，胜算更高一点。**

## 2. Submitter Type（必填，下拉）

选 **最接近你情况的**：
- 有 "Individual" 就选它
- 有 "Student" 也可以（你是本科生，个人参赛）
- 如果有 "Personal" / "Solo" 同理

## 3. Organization Name (if applicable)（必填）

```
N/A
```
（个人参赛，不代表任何组织）

## 4. Submitter Country of Residence（必填，下拉）

选 **China**。

## 5. If you or any team members reside in Canada, indicate the province（必填）

```
N/A
```
（不在加拿大）

## 6. Which track are you submitting your project into?（必填，下拉）

```
Physical AI
```

## 7. Is your project new or existing prior to August 26, 2026?（必填，下拉）

```
New
```

> **为什么是 New**：这个仓库的第一个 commit 是 **2026-10-22**，
> 晚于提交期开始的 8 月 26 日，所以不属于"期初已存在"的项目。
>
> 下面那个 "If your project is existing, explain how you significantly
> updated..." 的框在选 New 之后**不用填**。

## 8. Provide a URL to your public code repository（必填）

```
https://github.com/ASylviaofmine/nemotron-nav-agent
```

> 字段要求包含三点，仓库都已满足：
> - ✅ OSI 许可（MIT，在 About 栏可见）
> - ✅ README 有安装和运行说明
> - ✅ README 开头就写明用了 NVIDIA Nemotron + Token Factory

## 9. Provide a URL to a working demo（**不要求**）

```
留空
```
（字段自己写着 *"Not required for Physical AI submissions"*）

如果想填，填仓库里的视频：
```
https://github.com/ASylviaofmine/nemotron-nav-agent/blob/master/docs/submission.mp4
```

## 10. Which model(s) did you use, and why did you choose that size/variant?（必填）

**用这个短版（719 字符）**。字段提示写着 "e.g., Nemotron-4 340B, Nemotron-Mini, etc."，
问的是"哪个模型 + 为什么选这个尺寸"，不需要长篇。

```
NVIDIA Nemotron 3 Super 120B-A12B (nvidia/nemotron-3-super-120b-a12b) via
Nebius Token Factory.

The task is small and well specified -- read measured error metrics, name
which error source dominates, propose one clamped parameter change -- so
the bottleneck is instruction-following and numeric discipline, not
knowledge. Super was chosen because the proposal must be numerically
legal: an out-of-range value gets clamped and the suggestion is wasted.

The price decided it too: a full evaluation is about 30 short calls, a
fraction of a cent, cheap enough to iterate on the prompt and the
evaluation protocol. Nemotron 3 Nano 30B-A3B would be the right pick for a
cheaper "name the error source" variant of this task.
```

> **长版在这里不需要。** 原来那版 1200+ 字符是按"评奖反馈"写的，
> 但这个字段是**事实性**的。真正需要长篇的是下面那几个反馈字段
> （输出质量评分、与其他模型对比、想要什么改进）—— 那些才是
> "Most Valuable Feedback" 评奖内容。

## 11. How would you rate Nemotron's output quality for your use case? (1-10)（必填）

**评分：7**

> 这个字段开始就是**反馈评奖内容**了，用长版。

```
7/10 for this use case.

What worked well: instruction-following and numeric discipline. The
model reliably returned a diagnosis and a proposed change in the
requested structure, proposed values inside the legal range rather than
outliers, and -- importantly -- correctly proposed *no change* when the
error was already inside tolerance. That last one is the behaviour I
care about most: a model that always proposes something would have been
useless here, because the loop measures the result and discards changes
that do not help. Recognising "there is nothing left worth changing"
is a real sign of reading the numbers rather than performing.

What fell short: the model was better at *naming* the dominant error
source than at reasoning about *why* the gain was low. The diagnosis
("cross-track error dominates the residual; the heading gain is too low
for the requested speed") was the valuable part. The proposed value
was plausible but not insightful -- Kp = 12 happened to be good, and
the model arrived at it more by pattern-matching a "too low" diagnosis
than by working out what the gain should be. A model that could
predict the *effect* of a gain change before trying it would be worth
more here.

I am rating the output, not the effort. The output was clean, legal and
useful as a starting point for a search. It was not, on this simulator,
better than the fixed rule in the control row, and my evaluation table
says so.
```

## 12. Did you fine-tune, prompt-engineer, or use Nemotron out of the box?（必填）

```
Out of the box, with prompt engineering only. No fine-tuning, no
RAG, no LoRA -- none of it was needed, and I would argue it would have
made the project worse.

The prompt does three things and nothing else: it states the task
(diagnose the tracking error and propose one parameter change), it
lists the current parameters and the legal range for each, and it asks
for the response in a fixed structure (a diagnosis string plus a JSON
object of proposed changes). Everything else is enforced in code, not
in the prompt: the proposed values are clamped to their legal ranges
before they are applied, an empty change set is treated as "stop", and
the simulation is re-run to decide whether the change was kept.

That division is the point of the project. The model is never trusted
to produce a legal, safe or beneficial action -- it is trusted to
produce a *guess*, and the code decides whether the guess survives.
Prompt engineering shaped how well it guesses. It could never have
changed whether a guess was accepted.

What I did change, and would change again, is the system prompt. The
first version included the tuning heuristics explicitly, so the model
was mostly re-deriving what I had already written down. The version I
shipped describes the *situation* and the *available knobs* and lets
the model decide what to try. That version produced the diagnoses I
kept; the first one mostly restated the prompt.
```

## 13. How did Nemotron's performance compare to other models you've used for similar tasks?（必填）

```
I have used GPT-family models for code generation and structured
extraction, and I have used smaller open models locally. On the tasks
that overlap with this one -- turning a pile of numbers into a
structured recommendation -- Nemotron 3 Super was at least as good as
what I have used elsewhere, and better on one specific axis: it
produced a *justified* recommendation rather than a bare one.

The honest caveat is that I did not run a controlled comparison. I
have no side-by-side numbers for the same prompts across models, so
"at least as good" is an impression from use, not a measurement. I
would not want to present it as more than that.

Where I did notice a difference is latency and cost against the local
models I have used. The local models are free but need a GPU I do not
have, and their quality on numeric reasoning was noticeably worse.
The Nemotron-hosted models were fast enough to sit inside a tuning
loop -- which is the only reason the loop is practical at all, because
a slow model would make each measured iteration expensive and the
whole point is to iterate.

One thing I could not test: whether the newer, larger Nemotron
variants would be meaningfully better here. I picked Super 120B
because the pricing made iteration free; I did not have the budget to
also run an Ultra comparison and measure it.
```

## 14. Which Nebius platform capabilities were most valuable and how?（必填）

```
Token Factory's OpenAI-compatible inference API, and specifically the
serverless, pay-per-token access to Nemotron 3 Super 120B.

The capability that made this project possible was not a GPU choice
or a deployment setup -- it was that a 120B-class model was reachable
through an ordinary HTTPS endpoint with an API key, at a price that
made an iterative loop affordable. A full evaluation run is roughly 30
short calls and costs a fraction of a cent. I ran the evaluation
dozens of times while developing the prompt and the metrics, and each
of those runs cost less than a coffee. That is the whole reason the
measurement discipline in the repository exists: I could afford to
check.

Three concrete ways the platform was used:

1. API access: the OpenAI-compatible Chat Completions endpoint at
   api.tokenfactory.nebius.com/v1, authenticated with a bearer token.
   My client is written against the standard library (urllib) on
   purpose -- one less package that can fail to install, which means
   the repository is reviewable by a judge before they have an
   account, and the offline fallback works everywhere.

2. Model discovery: the client queries /v1/models at runtime and falls
   back through a list of candidate model IDs on a 400 or 404. This
   exists because the model IDs are spelled inconsistently across
   Nebius's own documentation pages, and I would rather the project
   degrade gracefully than fail on a first call.

3. Scaling: not needed here, and I want to be precise about that. The
   evaluation runs a 125-combination sweep and a 10-map suite, which
   is embarrassingly parallel and would be the obvious fit for
   Serverless Jobs -- but a single machine finishes it in under a
   minute, so running it on cloud jobs would have been theatre. Where
   it would earn its place is a suite of hundreds of maps.

Not used: AI Cloud deployment. The Physical AI track does not require
it, and the requirement here is satisfied by the runtime Token Factory
call rather than by hosting. Deployment would have added a moving part
without adding evidence.
```

## 15. How likely to recommend running Nemotron on Nebius? (1-10)（必填）

**评分：8**

```
8/10, and I would recommend it specifically to anyone building a
measured, iterative system around a model -- which is a narrower
recommendation than "use Nemotron for everything".

Why: the combination that made this project work is inference cheap
enough to sit inside a loop. A full evaluation costs a fraction of a
cent, which means the model can be consulted dozens of times per
experiment without the cost being a design constraint. Most "LLM in
the loop" ideas die because each iteration costs something; here the
iteration was free, and that is what let the evaluation protocol itself
be iterated on instead of being frozen on the first try.

The API being OpenAI-compatible is a real, unglamorous advantage. My
client needed no SDK, no special streaming semantics and no
vendor-specific object format, which kept the integration small enough
that the interesting part of the repository is the control loop rather
than the plumbing.

Why not 10: the model-ID inconsistency in the documentation cost more
debugging time than the rest of the client put together, and I would
not want to recommend a platform on the strength of a first call
failing. The docs and the /v1/models list disagree about the canonical
form, and for a builder following the quickstart in order that is a bad
first experience. It is a documentation problem rather than a platform
problem, but it is the first thing a new user hits.

Second, a caveat about the workload: Nemotron was very good at
*framing* a diagnosis from metrics and much weaker at predicting the
*effect* of a change. If your use case is "produce the final answer",
you may want to test a bigger variant. If it is "propose a candidate
that a simulator will verify", this setup is a good fit.
```

## 16. How would you rate your experience running Nemotron inference on Nebius vs previous cloud or local environments? (1-10)（必填）

**评分：8**

```
8/10 compared with both the cloud APIs and the local models I have
used.

Better than local: no GPU, no model download, no dependency on
anything but an API key and the standard library. My project depends on
zero third-party packages for the inference path, which means it
installs and runs anywhere with Python. The quality difference against
the small local models I have used was decisive for anything involving
numeric reasoning.

Better than the cloud APIs I have used: the cost model, and the fact
that Nemotron models are served on the same endpoint as everything
else, so there was no vendor-specific SDK, streaming protocol or
object format to learn. The client is 60 lines of urllib. Comparing
that to the setup work for other hosted models is stark.

What held it back from a 10, in order of how much it actually cost me:

1. The model IDs in the documentation do not match the model IDs the
   API returns. I found at least three spellings across Nebius's own
   pages, and the one in the quickstart is not the one that works. My
   first call 404'd, and nothing in the error message said "your ID is
   spelled differently here" -- so I spent real time wondering whether
   my code was wrong. The fix in my client is to query /v1/models and
   fall back, but that is a workaround for the documentation, and it
   should not have been necessary.

2. There is no way to ask "which model is the cheapest one that can do
   this?" The pricing page lists models and prices, but a builder
   choosing between Super and Nano has to work it out from a table.
   A one-line recommendation per model ("Nano for classification, Super
   for anything with numeric reasoning") would have saved me a
   decision.

3. /v1/models is not mentioned in the quickstart, and it is the only
   source of truth that actually agrees with the API. One sentence
   pointing at it would have saved me the fallback code entirely.

The one thing I would change beyond documentation: a
schema-constrained response mode, so a model asked for a parameter
proposal returns a validated object rather than prose that has to be
parsed. I used a JSON-structured request plus clamping on my side,
which works, but a first-class mode would remove a whole category of
failure from the "LLM in the loop" pattern -- and that pattern is where
I think this platform is most valuable.
```

## 17. What additional features or improvements would have made the experience more effective?（必填）

```
Three, in order of how much they would have helped this project.

1. A canonical, documented list of model IDs in the quickstart. At
   least three spellings are in circulation across Nebius's own pages,
   and the quickstart's is not among the ones that work. The API
   itself is fine -- it is the documentation that sends people the
   wrong way. Publishing the exact strings that /v1/models returns for
   the Nemotron family, and saying which form is canonical, would
   remove the single largest source of friction I hit.

2. A schema-constrained response mode. Asking for a parameter proposal
   and getting back prose that has to be parsed and clamped is a
   source of silent failure. If the endpoint could be told "respond
   with JSON matching this schema, or return an error", the "LLM in the
   loop" pattern becomes much safer to build -- particularly for
   anyone doing what I did, where a malformed or out-of-range value
   has to be caught before it is applied.

3. A "cheapest model that can do this" recommendation per model. The
   pricing page is a table; a one-line guidance ("Nano for
   classification, Super for numeric reasoning") would save a
   cost/quality judgement on every project.

Smaller ones: streaming support was not needed here but I assume it
exists; and an explicit "this model is deprecated, use X" signal would
have helped the fallback logic, since a 404 is ambiguous between "typo"
and "model withdrawn".
```

## 18. What do you most hope to see from the Nemotron team next?（必填）

```
I would like to see the smaller variants get better at the kind of task
this project needed, because that is where the cost/quality trade
decides whether a pattern is usable in production.

Concretely: a model in the Nano class that reliably returns a
*numerically legal* structured proposal, and that knows when to propose
nothing. The second part is the harder and more interesting one. My
loop only works because a wrong suggestion is cheap -- but the loop
only converges because the model sometimes says "there is nothing left
to change here". A small model that over-proposes is not merely
inaccurate, it is actively harmful in this pattern, because it burns
iterations on changes the measurement will discard. Teaching the
models to be comfortable with "no change needed" feels like a
high-value capability for the supervised-optimisation use case, and it
is not something I have seen benchmarked.

Second, I would like a documented, canonical model registry -- a
single endpoint that says which model IDs are current, which are
deprecated, and what each one is good at. Not a benchmark table: a
recommendation. "For anything with numeric reasoning, start here" is
more actionable than a leaderboard.

Third, and most selfishly: I would like to see the evaluation story
strengthen on the physical side. The Physical AI track is full of
projects that will end up with a simulation and a plausible number, and
the hard part -- building the control loop that makes a suggestion
verifiable -- is the part nobody writes down. If Nemotron or Nebius
published reference patterns for "model proposes, physical system
disposes", the gap between a demo and a deployable system would close
faster for everyone.
```

## 19. Did you use Tavily in your project?（必填，下拉）

```
No
```

> 规则原文：*"To qualify: your project must make a functional, runtime
> call to the Tavily API as part of its solution."*
> 这个项目**没有**用 Tavily——它不需要联网搜索。选 No 是诚实的。
> （有独立的 "Best Use of Tavily" $3,000 奖项，但那是给用 Tavily 的人准备的。）

## 20. Builders & Brews - IRL Events City（下拉）

```
不选 / 留空
```
（除非你参加过某个城市的线下活动。选错了会影响 City Winner 资格判定。）

## 21. 两个 checkbox（必打勾）

```
☐ I, and if applicable, all of my teammates, are at least the age of majority where I reside (e.g. 18 in the US).
☐ I, and if applicable, all of my teammates, are not employees, representatives nor agents of the Promotion Entities of this hackathon.
```

**两个都要勾。** 个人参赛的话第 2 条显然成立。

## 22. Which AI tools have you leveraged while working on this project?（必填）

**用这个中等长度版（约 900 字符）**。这个字段是"列出来"的性质，
写太长会喧宾夺主——但如实写比假装全程手写更可信。

```
An AI coding assistant, for the parts of the work where a language model
is genuinely better than typing: reading unfamiliar code, restructuring
files, and hunting the kind of bug where a label and the value it prints
disagree. The bug I remember is the video renderer printing an
*instantaneous* error under a label that said "max" -- I found it by
looking at a rendered frame, not by reading the code.

What I deliberately did not delegate, because these are the parts that
make the project credible: the metric definition (cross-track error had
to be measured to the planned polyline, not the nearest waypoint -- the
wrong one hides the effect of every parameter); the evaluation design
(the no-model control row, the independent exhaustive reference, the
self-test); and every number in the README, each regenerated by a
script that I ran.

The pattern I ended up with: use the assistant for the mechanical parts
and the search for the bug, keep the judgement and the evaluation design.
The same verification loop that makes this project defensible applies to
my own work too -- an assistant that suggested a change to the metric
would have been as wrong as a model that proposed a bad parameter, and
reading the output would not have caught it.
```

## 23. Describe the level of learning you/your team derived from the project（下拉）

选**最高的那一档**。这个项目你确实学到了东西：
A\* 的可采纳性证明、角度 wrapping、指标定义、评测设计（对照组 + 穷举参照）、
prompt 工程与代码强制约束的分工、以及"验证回路"这个模式本身。

如果选项类似 "Significant" / "Substantial" / "Advanced" / "Expert"，
选最接近"**Significant**"或"**Advanced**"的那个。

## 24. Did you gain AI value that you can use in your career?（必填，下拉）

```
Yes
```

> 选 Yes 就行，不用展开——但如果有补充说明框，可以写：
> The pattern -- an LLM proposes, the system verifies, the measurement
> decides -- is how I will think about putting models in front of
> physical or safety-relevant systems from now on.

# ⬆️ 复制粘贴区结束 ⬆️

---

## 关于评分的三点说明

我给的分数是 **7 / 8 / 8**，理由都写在各自的说明里了。

给 7 而不是 9-10 的原因：模型在**给出诊断**上确实好用，但在**预测改动效果**上
明显弱（Kp=12 更像是模式匹配"太低了"这个诊断，而不是推导出来的）。而且
它**没有打败**我自己写的固定规则——这一点我的评估表里明明白白写着。

给 8 而不是 10 的原因：文档里的模型 ID 拼写不一致，我第一次调用就 404 了，
排查花的时间比写完整个 client 还多。这不是平台能力问题，是文档问题，
但它是新用户撞到的第一件事。

**这些"缺点"是加分项，不是减分项。** 反馈奖评的是 completeness /
viability / potential impact——一个只说"很好用"的反馈是零分；
一个能说清"哪里好用、哪里不好用、为什么、我会怎么改"的反馈才是满分候选。
