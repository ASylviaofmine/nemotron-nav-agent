# 视频剪辑指引 — 照着做，5 分钟

## 先说结论：你**几乎不需要剪**

| 你可能会想剪 | 实际要不要 |
|---|---|
| 剪掉不重要的片段 | **不用**。81 秒里每一秒都是关键模块在动，正合规则 |
| 加转场特效 | **不用**。规则禁止无授权素材，特效只会扣分 |
| 配背景音乐 | **不用**。规则明确禁止版权音乐 |
| 加旁白 | **可选**。规则只要 footage（画面），视频里已有文字标注 |
| 加英文字幕 | **推荐**。如果你的解说用中文，规则要求英文字幕；直接写英文字幕最省事 |
| 调色 / 变速 | **不用** |

**最省事的完整流程（5 分钟）**：

1. 打开 https://studio.youtube.com
2. 上传 `docs/submission.mp4`
3. 可见性选 **Public**（必看下面）
4. 标题和描述粘贴 `docs/VIDEO_SCRIPT.md` 里的现成文案
5. 发布

**这样交上去的视频完全合规**，因为规则原文只要求：
> *"footage that shows the Project functioning"*
> *"Physical AI submissions should include at least one minute of footage showing ... the key application modules in action"*

你的视频有 **81 秒**，远超"至少 1 分钟"，且每一秒都是真实仿真画面在动。

---

## 视频里有什么（你不需要重新了解，直接对照）

| 时间 | 画面 | 说明 |
|---|---|---|
| **0:00–0:06** | 标题卡 | 项目名 + 一句话说明 + 右侧地图 |
| **0:06–0:17** | A\* 逐格找路 | 路径一格格延伸，然后机器人沿路径行驶 |
| **0:17–0:52** | **基线 vs 调优 + 实时误差曲线** | ← 最重要的一幕。红线震荡到 0.0895 m，绿线几乎贴地 0.0233 m |
| **0:52–1:03** | 10 图套件条形图 | 每组红（基线）长、绿（调优后）短 |
| **1:03–1:13** | 模型诊断 + Why the loop stopped | 模型说了什么，以及为什么它停手 |
| **1:13–1:21** | 结论表 + 穷举参照系 | 三行数字：基线 / 模型之后 / 125 组穷举最优 |

技术参数：1000×700，20fps，81 秒，8.2 MB。

---

## 方案 A：直接上传（推荐，5 分钟）

### 第 1 步：上传

打开 **https://studio.youtube.com** → 右上角 **Create** → **Upload videos**
→ 拖入 `docs/submission.mp4`

文件路径（两个位置都有）：
```
C:\Users\Lee\WorkBuddy\2026-10-21-22-18-37\nemotron-nav-agent\docs\submission.mp4
C:\Users\Lee\PycharmProjects\nemotron-nav-agent\docs\submission.mp4
```

### 第 2 步：填信息

**Title**（不超过 100 字符）：
```
nemotron-nav-agent — a Nemotron model supervises a robot's tracking controller
```

**Description**：直接复制 `docs/VIDEO_SCRIPT.md` 末尾那段（里面已含仓库链接和复现命令）。

### 第 3 步：可见性 —— **这一步最容易出错**

上传后默认是 **Private**。点 **Visibility** → 选 **Public**。

| 选项 | 行不行 |
|---|---|
| **Public** | ✅ 选这个 |
| Unlisted | ⚠️ 规则说 "public or unlisted" 技术上可以，但评委点链接可能打不开，**建议 Public** |
| Private | ❌ **绝对不行**，评委看不到 |

上传完成后**去视频页面确认一次**：地址栏能直接打开、右上角显示"Public"。

### 第 4 步：发布

点 **Next** → 检查缩略图（YouTube 会自动选一帧，可以换成你指定的那张）→
**Visibility 确认是 Public** → **Publish**。

> 缩略图建议：YouTube 让你三选一（自动帧 / 中间帧 / 结尾帧）。选**中间帧**（约 40 秒）
> 大概率就是基线 vs 调优的对比画面——就是最该被看到的那一幕。
> 想更准的话，先自己上传 `docs/thumbnail.png` 作自定义缩略图（YouTube 支持）。

---

## 方案 B：加英文字幕（如果你想要更稳，30 分钟）

规则原文：
> *"All Submission materials must be in English or, if not in English, the Entrant must provide an English translation of the demonstration video..."*

**如果你不配任何解说，这个问题不存在**（视频本身没有语言）。
**如果你配了中文解说，就必须加英文字幕。**

### 用剪映 / CapCut 的步骤

1. 新建项目 → 导入 `docs/submission.mp4`
2. 点 **文本** → **自动字幕** → 识别语言选 English
   （注意：视频里没有语音，只有文字，所以**自动字幕会识别不出东西**）
3. **正确做法**：手动打字幕。用下面这段文本，按时间轴贴上去

### 现成的英文字幕（照着贴，一句一条）

| 时间 | 字幕 |
|---|---|
| 0:00 | nemotron-nav-agent |
| 0:03 | A wheeled robot that plans with A* and tracks with a proportional controller, supervised by an NVIDIA Nemotron model on Nebius Token Factory. |
| 0:07 | First, A* finds the route around the wall. |
| 0:13 | The robot then follows it with a proportional heading controller. |
| 0:18 | This is the core of the project: the same task, tracked twice. |
| 0:22 | Left: the baseline parameters. Right: the parameters the model chose. |
| 0:27 | The plot under each panel is the measured cross-track error, drawn live. |
| 0:33 | The red curve climbs to five centimetres and keeps oscillating. |
| 0:38 | The green one stays near the floor. And the tuned run finishes slightly faster. |
| 0:53 | Does it generalise? The same loop over a seeded suite of maps. |
| 0:58 | Every bar pair is one map. It improves on all of them. |
| 1:04 | What the model actually says. Round one: cross-track error dominates the residual. |
| 1:09 | It proposes raising Kp from five to twelve. |
| 1:13 | That is a hypothesis, not a result. The simulator re-runs, and the measurement decides. |
| 1:19 | The model supervises the parameters. The simulator decides. |

> **字幕只放底部一行，别做成花字。** 评委扫一眼就能看清，复杂的字幕反而挡画面。

### 导出设置（重要）

| 项 | 值 |
|---|---|
| 分辨率 | 1000×700 或 1920×1080 都行（**保持 16:9 附近的原比例，别拉伸**） |
| 帧率 | 20 fps（和原片一致） |
| 格式 | MP4 (H.264) |
| 音频 | 可以没有音轨（**不要加音乐**） |

> ⚠️ **千万别把 1000×700 拉伸成 16:9**（会变成 1000×562 上下留黑边，
> 或者 1280×700 被横向拉胖）。原样上传最省事。

---

## 上传后必须做的 3 个检查

- [ ] 打开视频链接（**无痕窗口**，确认不是只有你能看）→ 应该是 **Public**
- [ ] 时长 **> 60 秒**且 **< 3 分钟**（你是 81 秒）
- [ ] 前 30 秒就看懂这是什么（标题卡 + A\* + 对比画面，够了）

然后把链接填到两个地方：
1. **Devpost 表单**的 Demo video URL 字段
2. **README.md** 顶部（发我链接，我改好推送）

---

## 常见问题

**Q: 需要出镜吗？**
不需要。规则只要 "footage"，你的视频全是仿真画面和文字。

**Q: 会不会被判为"没有物理硬件所以不合格"？**
不会。规则原文针对无硬件项目写的是
*"or — if your project has no physical hardware component — the key application modules in action"*。
你的视频正是在展示关键模块（规划、跟踪、模型诊断、验证）在动。

**Q: 视频里没有声音会有问题吗？**
不会。规则没要求音频。

**Q: YouTube 会不会因为"无人声"而降低推荐权重？**
可能会影响推荐，但**不影响参赛评审**——评委点开链接看内容，不看推荐量。

**Q: 如果上传后发现视频有黑边/变形？**
删掉重传原文件，别用剪辑软件重新导出。原始 `submission.mp4` 是干净的。

**Q: 上传要多久？**
8.2 MB，家宽几秒到几十秒。
