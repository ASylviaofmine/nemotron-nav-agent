# 三个还空着的框 —— 都是 5 分钟的事

## 1. 仓库 Description 和 Topics（GitHub）

**在哪**：打开 https://github.com/ASylviaofmine/nemotron-nav-agent
→ 页面**右上角**（Releases / Packages 那一行下面）有一栏叫 **About**
→ 最右边有个 **⚙️ 齿轮图标**，点它。

### Description

填这一句：

```
A wheeled robot that plans with A* and tracks with a proportional controller, supervised by an NVIDIA Nemotron model on Nebius Token Factory.
```

### Topics

点 **Topics** 旁边的 **Edit**，逐个加（每个都要点一下搜索框选）：

```
nvidia
nebius
nemotron
robotics
physical-ai
python
```

### Homepage（可选，锦上添花）

```
https://devpost.com/software/nemotron-nav-agent
```

> 填了它，仓库右上角会出现一个链接按钮，评委点仓库能直接跳到 Devpost 项目页。

### 为什么值得填

- **Description 是评委打开仓库后第一眼看到的文字**（在搜索结果里也是它）
- **Topics 是搜索权重** —— 评委按 "nvidia" "physical-ai" 搜项目时能不能搜到你
- 规则里明确要求 README 要 *"highlight how you've used NVIDIA Nemotron"*
  —— Description 写清楚这一点，正好呼应

**我做不了这一步**：GitHub API 需要 Personal Access Token，这台机器上没存。
SSH 密钥只能推送代码，改不了仓库设置。

---

## 2. "Describe your contribution"（Devpost，截图右边那个框）

**在哪**：你截图里 **CREATED BY** 那一栏，框里现在显示的是灰色斜体占位文字
*"Ex: I worked on the back-end. It was my first time using Node..."*
—— 那是**提示示例，不是你写的内容**。它现在是空的。

**这个框会出现在你的公开项目页上**，评委能看到。填：

```
Solo project. I wrote the A* planner, the proportional controller, the
simulation, the cross-track error metric and its self-test, the Token
Factory client, the supervision loop, the evaluation harness and the
video renderer -- all of it, start to finish. The NVIDIA Nemotron model
on Nebius Token Factory supplies the diagnoses; every number in the
write-up is produced by a script in the repository.

The evaluation was the part I cared about most. A model that cannot be
checked against a measurement is a model that cannot be evaluated, so
the framework keeps only the changes the simulator says helped -- and
the write-up reports the row where the model did not beat a fixed rule,
because a judge should be able to check that too.
```

---

## 顺序建议

1. **换 YouTube 视频**（30 分钟，最要紧 —— 字幕重叠是评委打开就看到的）
2. **改 Devpost 的 Video URL**（视频 ID 会变）
3. **填 "Describe your contribution"**（截图那个框）
4. **填 GitHub Description + Topics**（5 分钟）
5. **README 视频链接**（发我新链接，我改好推送）

---

## 顺便：Devpost 上已经完成的部分

我拉了公开页面确认，以下全部正常：

- ✅ 标题 + elevator pitch 正确显示
- ✅ Project Story **全文 7 节**都上去了（Inspiration / What it does /
  How we built it / Challenges / Accomplishments / What we learned / What's next）
- ✅ 三行结果表格（基线 / 模型之后 / 125 组穷举最优）
- ✅ 代码块、引用块都正常渲染
- ✅ Built With 标签 10 个（automation / benchmarking / evaluation / gradio /
  numpy / opencv / pillow / python / robotics / simulation）
- ✅ 视频已嵌入，能播放
- ✅ 公开页面 https://devpost.com/software/nemotron-nav-agent 已上线
- ✅ "4 more days to submit" —— **还可以继续编辑**（点 Edit hackathon submission）

**Story 里那些内容我核对过，一个字没漏。** 现在要修的只有视频。
