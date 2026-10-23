# 提交清单 — 一步步照着做

距离截止（**2026-10-31 01:00 GMT+8**）还有 7 天多，不慌。
代码、视频、文档都已就绪，**只差把仓库传上去 + 录视频 + 填表**。

---

## 第 1 步：建 GitHub 仓库（2 分钟，只能你做）

打开 **https://github.com/new**

| 填什么 | 值 |
|---|---|
| Owner | `ASylviaofmine` |
| Repository name | `nemotron-nav-agent` |
| Description | `A wheeled robot that plans with A* and tracks with a proportional controller, supervised by an NVIDIA Nemotron model on Nebius Token Factory.` |
| Visibility | **Public** ← 必须，否则评委打不开 |
| README / .gitignore / license | **全部不要勾** ← 勾了会和本地冲突 |

点 **Create repository**。

> 为什么这一步必须你来：建仓库要调用 GitHub API，需要一个 Personal Access
> Token。这台机器上没有存 token，GitHub 连接器也没连上。你的 SSH 密钥只能
> 推送，**不能创建仓库**。

---

## 第 2 步：推送（我来做，你告诉我一声就行）

仓库建好后跟我说一声，我跑：

```bash
bash tools/publish.sh
```

脚本会设好 remote、推 `master` 分支、并给你链接。

---

## 第 3 步：给仓库补两样东西（1 分钟）

在 GitHub 仓库页面：

1. 右边栏 **About** → 齿轮图标 → 填 Description（和上面一样）→ **Topics** 加：
   `nvidia` `nebius` `nemotron` `robotics` `physical-ai` `python`
2. 右边栏 **Releases** → 不用管

> Topics 和 Description 是评委**第一眼**看到的搜索关键词，别省。

---

## 第 4 步：录 YouTube 视频（30 分钟）

素材已经做好：`docs/submission.mp4`（1000×700，**67 秒**，5 个场景）。

规则要求：
- 公开可见（不能是"不公开"）
- **少于 3 分钟**
- Physical AI 赛道：**至少 1 分钟**要展示关键模块在动 ← 67 秒正好达标

### 怎么录

**方法 A（最快，推荐）**：浏览器打开这个 GIF，录屏。

```
docs/submission.gif
```

用系统录屏（Win + Alt + R）录浏览器播放它的过程，1 分钟出头就够。
建议同时**配一段英文解说**（念场景标题即可），
或者加英文字幕 —— 规则要求"若非英文须提供英文字幕"。

**方法 B**：把 `submission.mp4` 上传到 YouTube（设为"公开"），
再在视频编辑器里加英文解说轨。

### 解说词可以直接用（对应视频里的场景）

> **Scene 1** — A* finds the route. Four-connected grid, Manhattan
> heuristic, unit step cost. The wall in the middle has two gaps, so the
> planner has to detour.
>
> **Scene 2** — This is the core of the project. The same task, tracked
> twice. On the left, the baseline parameters. On the right, the parameters
> the model chose. The plot underneath each one is the measured cross-track
> error, live. The red curve oscillates; the green one stays near the
> floor.
>
> **Scene 3** — The same loop over a seeded suite of maps. Every bar pair is
> one map. It improves on all of them.
>
> **Scene 4** — What the model actually says. A diagnosis, and a proposed
> change — clamped, applied, re-run, and kept only if the measurement
> improved.
>
> **Scene 5** — The claim, and the check. The exhaustive sweep of all 125
> parameter combinations involves no model at all, so it is an independent
> reference rather than a restatement of what the agent did.

录完把链接填到提交表和 README 顶部。

---

## 第 5 步：填 Devpost 表单（30 分钟）

`docs/SUBMISSION_DRAFT.md` 里每个字段的英文草稿都写好了，直接复制。

| 表单字段 | 填什么 |
|---|---|
| Title | `nemotron-nav-agent` |
| Description | 草稿里的长文 |
| Track | **Physical AI** |
| Repository URL | `https://github.com/ASylviaofmine/nemotron-nav-agent` |
| Demo URL | **留空**（Physical AI 赛道明确不要求） |
| Video URL | 你的 YouTube 链接 |
| Nebius/NVIDIA feedback | 草稿里那段（写得很诚实，见下） |
| Team | `ASylviaofmine`（个人参赛；想组队就现在加，队长才能按提交） |

### 关于 feedback 字段的写法

我在草稿里**没有吹牛**。规则原文是"Provide feedback on Nebius Token
Factory, AI Cloud and any NVIDIA tools"，所以实话最好。我写的是：
模型 ID 在官方文档里拼写不一致（这是真事，值得吐槽）、
模型真正帮上忙的地方是"把诊断说清楚"而不是最终数值、
以及**诚实地说明没打败精心编写的启发式**——因为评估表里本来就有那一行。

这种诚实反而更有可能赢，因为评委看得出来什么是真的。

---

## 第 6 步（可选但建议）：live 数字

拿到 `NEBIUS_API_KEY` 之后：

```bash
export NEBIUS_API_KEY=nb-...
python main.py tune
python tools/agent_eval.py
```

这会生成**真模型**跑出来的数字。把它替换进 README 的表格。

**为什么值得做**：现在的 README 表格标注了"离线 mock"，
智能体那几行和对照行**按构造完全相同**。有了 live 数字，
才能证明模型确实打败了无模型对照 —— 这就是整个项目的核心论点。

---

## 第 7 步：提交之后还能做什么（不是必需的，但值得知道）

先说清楚：**提交完就结束了。** 比赛到这里就截止了，没有"二轮评审"
或"补充材料"环节。规则里唯一还要求你做的事，是：

> "The Entrant must make the Project available free of charge and without any
> restriction, for testing, evaluation and use by the Sponsor, Administrator
> and Judges **until the Judging Period ends**."

也就是说，**仓库要保持公开可访问，直到评审结束**。别在提交后把仓库设成
私有或删掉，那是唯一的技术性"后续义务"。

那"上传完还能做什么"？分两种：

### A. 对这次比赛（提升分数的补救动作）

如果时间还有，**优先级从高到低**：

1. **补 live 数字**（第 6 步）—— 直接影响"技术实现"和"创意质量"两项。
2. **录完视频后看看自己的视频** —— 确认字幕能看清、没有超过 3 分钟、
   开头 10 秒就讲清楚这是什么。评委常只看前 30 秒。
3. **把仓库 Description 和 Topics 填好** —— 搜索权重，5 秒钟的事。
4. **如果评委在评论区提问**，及时回。规则里明确说了
   "Judges are not required to test the Project" —— 意思是很多评委**不会**
   真的 clone 跑一遍，只看文字、图片和视频。所以**文字和视频的质量，
   比代码跑不跑得起来更重要**。

### B. 对你自己（这个项目的真正价值）

这个仓库对**申请 Erasmus 奖学金 / 找实习**的价值，可能比比赛本身更大：

- 它证明你能**从零设计一个可评测的系统**，而不是调 API 拼界面。
  面试官问"你怎么知道它真的有效"，你的答案是"我跑了个穷举参照系，
  它落在 0.009 m 以内"——这种回答很难伪造。
- 它有一个**诚实的失败分析**（模型没打败启发式）。
  招人的导师更认这种能承认边界的人。
- 它跨了**经典算法 + 工程 + LLM 编排 + 评测方法论**四层，
  简历上可以写得很具体，不是"会用 LLM"这种空话。

**建议**：提交完之后，把 README 再润一遍，删掉比赛相关的话
（"for the hackathon" 之类），改成一个独立的项目 README。
比赛是一次性的，仓库是可以长期挂在简历上的。

---

## 常见问题

**Q: 视频必须我自己出镜吗？**
不需要。规则只要求 "footage that shows the Project functioning"。
录屏 + 字幕就够。但如果加英文解说，可信度会高一些。

**Q: demo URL 真的可以留空吗？**
可以。规则原文：*"not required for Physical AI submissions"*。
但如果你后来部署了 Gradio demo，填上去也不吃亏。

**Q: 提交之后还能改仓库吗？**
可以，规则没禁止。改了反而更好——说明项目在持续演进。
但**别改到评委看到的是另一回事**（比如把 demo 删了）。

**Q: 万一 Token Factory 账号最后没开通怎么办？**
README 里已经诚实标注了"离线 mock"模式，仓库**完全可运行**、
不依赖任何 API key，评委 clone 下来 `python tools/selftest.py` 就能看到
所有数字。这是当初就设计好的，不是事后补救。


不过这是**锦上添花**，不是必需项。仓库和视频没有，别的都白搭。

---

## 提交前最后检查

- [ ] 仓库是 **Public**，有 **MIT** 许可文件（`LICENSE` 已在仓库里）
- [ ] `README` 是仓库首页第一眼看到的东西
- [ ] Description 和 Topics 都填了
- [ ] `python tools/selftest.py` 在新 clone 上通过
- [ ] `python tools/agent_eval.py` 能复现 README 里的数字
- [ ] YouTube 视频**公开可见**、< 3 分钟、≥ 1 分钟展示模块动作
- [ ] 视频链接已填进**表单**和 **README**
- [ ] 全部英文（视频若有中文解说，须加英文字幕）
- [ ] **在 2026-10-31 01:00 GMT+8 之前点 Submit**
