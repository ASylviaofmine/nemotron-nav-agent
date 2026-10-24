# 提交清单 — 一步步照着做

> **当前状态（2026-10-24 14:51，距截止 6 天 10 小时）**
>
> | # | 事项 | 状态 |
> |---|---|---|
> | 1 | GitHub 公开仓库 | ✅ **已完成** — public / MIT / 38 个文件 |
> | 2 | 仓库 Description + Topics | ⬜ **待做（5 分钟）** |
> | 3 | YouTube 视频 | ⬜ **待做（5-30 分钟）** ← 硬性要求 |
> | 4 | 填 Devpost 表单 + 点 Submit | ⬜ **待做（30 分钟）** |
> | 5 | live 数字（可选） | ⬜ 有 API key 再做 |
>
> **缩略图已做好**：`docs/thumbnail.png`（1000×700，103 KB）——
> 视频里最有说服力的那一帧，直接上传。

## 关键日期（官方 schedule 页，核实于 2026-10-24）

| 事件 | 时间（GMT+8） |
|---|---|
| **提交截止** | **2026-10-31 01:00** |
| 评审期 | 2026-12-02 01:00 → 12-16 04:00 |
| 获奖公布 | 2027-01-12 04:00 |

> 评审在 12 月、结果 1 月才出 —— 所以**仓库要一直保持公开**，
> 别在提交后改成私有。那是规则里唯一的后续义务。

## 值得知道的奖金结构

| 奖项 | 金额 | 与你的关系 |
|---|---|---|
| Grand Prize | $20,000 | 主奖，四维等权重 |
| **Physical AI Track Winner** | **$20,000 + NVIDIA Jetson Orin Nano** | ← **你的目标赛道** |
| **Most Valuable Feedback** | **$100 × 10 名 + NVIDIA 周边** | ← **反馈字段是独立评奖项！** |
| City Winner Awards | $500 × 20 | 只有参加过 Builders & Brews 才能报 |

**"Most Valuable Feedback" 是单独评奖的**（规则原文：按 completeness、
viability、potential impact 评估）。所以反馈字段不能写成"用起来还行"，
要写成**对其他构建者有用的、具体的、可执行的反馈**。
草稿已经按这个标准重写了。

---

## 一句话回答"要上传什么到比赛"

Devpost 那个网页**不是用来写代码的**，是**填表交作业**的。
你只需要交 **4 个链接 + 3 段文字**：

| 表单字段 | 填什么 | 状态 |
|---|---|---|
| **Repository URL** | `https://github.com/ASylviaofmine/nemotron-nav-agent` | ✅ 有了 |
| **Video URL** | 你的 YouTube 链接 | ⬜ 要先录视频 |
| **Demo URL** | **留空** | ✅ 不用填（Physical AI 赛道明确不要求） |
| **Track** | `Physical AI` | ✅ |
| **Project description** | 长文，草稿在 `SUBMISSION_DRAFT.md` | ✅ 复制粘贴 |
| **Nebius/NVIDIA feedback** | 中等长度，草稿在 `SUBMISSION_DRAFT.md` | ✅ 复制粘贴 |
| **Team** | `ASylviaofmine` | ✅ |

**最后点 Submit 才算提交。** 不点 = 没交。

---

## 第 1 步：建 GitHub 仓库 ✅ 已完成

仓库已存在且推送完毕。如果之后要改 Description / Topics，见第 3 步。

---

## 第 2 步：录 YouTube 视频

**素材已做好**：`docs/submission.mp4`，81 秒，5 个场景。

最省事的方式（**不需要出镜、不需要录屏**）：
1. 打开 https://studio.youtube.com
2. 上传 `docs/submission.mp4`
3. **可见性选 Public**（关键）
4. 发布

完整的录法、逐分镜解说词、YouTube 描述栏文案：
**看 `docs/VIDEO_SCRIPT.md`**

规则硬性要求：公开可见、< 3 分钟、**≥ 1 分钟展示关键模块动作**（你的是 81 秒实拍仿真画面，达标）。

---

## 第 3 步：填仓库 Description + Topics（5 分钟）

打开仓库页 → 右边栏 **About** 旁的齿轮：

**Description**
```
A wheeled robot that plans with A* and tracks with a proportional controller, supervised by an NVIDIA Nemotron model on Nebius Token Factory.
```

**Topics**（逐个点进去搜）
```
nvidia  nebius  nemotron  robotics  physical-ai  python
```

这是评委**第一眼**看到的东西，也影响搜索权重。别省。

---

## 第 4 步：填 Devpost 表单

`docs/SUBMISSION_DRAFT.md` 里每个字段的英文草稿都写好了，直接复制。

| 表单字段 | 填什么 |
|---|---|
| Title | `nemotron-nav-agent` |
| Description | 草稿里的长文 |
| Track | **Physical AI** |
| Repository URL | `https://github.com/ASylviaofmine/nemotron-nav-agent` |
| Demo URL | **留空**（Physical AI 赛道明确不要求） |
| Video URL | 你的 YouTube 链接 |
| Nebius/NVIDIA feedback | 草稿里那段 |
| Team | `ASylviaofmine` |

### 关于 feedback 字段的写法

草稿里**没有吹牛**。规则原文是"Provide feedback on Nebius Token
Factory, AI Cloud and any NVIDIA tools"，所以实话最好。我写的是：
模型 ID 在官方文档里拼写不一致（真事，值得吐槽）、
模型真正帮上忙的地方是"把诊断说清楚"而不是最终数值、
以及**诚实地说明没打败精心编写的启发式**——因为评估表里本来就有那一行。

这种诚实反而更有可能赢，因为评委看得出来什么是真的。

---

## 第 5 步：视频链接加回 README

视频上传后，把链接发我，我改 README 顶部并推送
（现在那里指向仓库内的文件，因为你的 YouTube 链接当时还不存在）。

---


## 第 6 步（可选）：live 数字

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
