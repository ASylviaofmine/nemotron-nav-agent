# 视频解说词（照着念，时间码精确到分镜）

素材：`docs/submission.mp4`（81 秒，1000×700，5 个场景 + 标题卡）
规则要求：公开可见、**< 3 分钟**、Physical AI 需 **≥ 1 分钟**展示关键模块动作 ← 81 秒达标

---

## 怎么录（选一个，5 分钟搞定）

### 方法 A：直接上传（最省事，推荐）

1. 打开 https://studio.youtube.com
2. 上传 `docs/submission.mp4`
3. 可见性选 **Public**（**关键**——"不公开"和"私有"都不算，评委打不开）
4. 标题：`nemotron-nav-agent — a Nemotron model supervises a robot's tracking controller`
5. 描述粘贴下面这段
6. 直接发布，不用配乐、不用录屏、不用出镜

> 这样交上去的视频**没有解说**，但**完全合规**——规则只要求
> "footage that shows the Project functioning"，没要求旁白。
> 而且视频里的文字已经把每个场景讲清楚了。

### 方法 B：加解说（更稳，推荐你有余力时做）

在方法 A 基础上，用剪映 / CapCut 打开视频，按下面的时间轴配英文字幕。
**注意**：如果你用中文解说，规则要求"若非英文须提供英文字幕"，
所以最省事是**直接写英文字幕**。

---

## 分镜时间轴 + 对应解说词

### 0:00 – 0:06 标题卡

画面：项目名 + 一句话说明 + 右侧地图

> **nemotron-nav-agent.**
> A wheeled robot that plans with A-star and tracks with a proportional
> controller — supervised by an NVIDIA Nemotron model on Nebius Token Factory.

---

### 0:06 – 0:17 场景①：A* 逐格找路

画面：10×10 网格，中间有墙，路径一格一格延伸，最后机器人沿路径行驶

> First the classical half: A-star finds the route around the wall,
> four-connected grid, Manhattan heuristic, unit step cost. The heuristic
> never overestimates, so the path is guaranteed shortest.
> Then the robot follows it with a proportional heading controller.

---

### 0:17 – 0:52 场景②：基线 vs 调优（**最重要的一幕**）

画面：左右并排两个仿真，下面各有一条实时误差曲线。红线反复震荡，绿线几乎贴地

> This is the core of the project. The same task, tracked twice.
> On the left: the baseline parameters. On the right: the parameters the
> model chose. The plot under each panel is the measured cross-track
> error, drawn live.
>
> The red curve climbs to five centimetres and keeps oscillating — the
> heading gain is too low for the requested speed. The green one stays
> near the floor. And notice: the tuned run finishes slightly *faster*.
> Better tracking, lower cost.

---

### 0:52 – 1:03 场景③：10 图套件条形图

画面：8 组横条，每组红（基线）长、绿（调优后）短

> Does it generalise? The same loop over a seeded suite of maps — a
> canonical wall map, a wall map with the openings moved, and six random
> obstacle maps. Every bar pair is one map. It improves on all of them.

---

### 1:03 – 1:13 场景④：模型说了什么

画面：两轮的诊断原文 + 实测数字 + "Why the loop stopped"

> What the model actually says. Round one: cross-track error dominates
> the residual, the heading gain is too low. It proposes raising Kp from
> five to twelve.
>
> That is a hypothesis, not a result. The change is clamped, applied, and
> the simulation is re-run — the measurement decides, not the model.
> Round two: the error is now inside tolerance, so raising the gain
> further would cost time without buying accuracy, and the model proposes
> nothing.

---

### 1:13 – 1:21 场景⑤：结论 + 穷举参照系

画面：三行表格（基线 / 模型之后 / 125 组穷举最优）+ 底部一行结论

> And the check. The third row is the best of all 125 swept parameter
> combinations — a deterministic sweep that involves no model at all.
> So "the agent landed within nine millimetres of the best of 125" is a
> claim a reviewer can verify by running one script.
>
> The model supervises the parameters. The simulator decides.

---

## YouTube 描述栏粘贴这段

```
nemotron-nav-agent

A wheeled robot that plans with A* and tracks with a proportional
controller — supervised by an NVIDIA Nemotron model on Nebius Token
Factory, for the Nebius x NVIDIA Global AI Hackathon (Physical AI track).

The model does not drive the robot. It reads the measured tracking error
and proposes the next parameter change; the simulator re-runs and keeps
the change only if the numbers actually improved.

Built for the Nebius Global AI Hackathon:
https://nebiusglobalaihackathon.devpost.com

Repository (public, MIT licensed):
https://github.com/ASylviaofmine/nemotron-nav-agent

Run it yourself -- the core needs only numpy and Pillow, no API key:

    git clone https://github.com/ASylviaofmine/nemotron-nav-agent
    cd nemotron-nav-agent
    pip install numpy pillow
    python tools/selftest.py
    python tools/agent_eval.py

With a NEBIUS_API_KEY set, the same scripts run the live Nemotron model
instead of the offline fallback.

Model: NVIDIA Nemotron via Nebius Token Factory
(nvidia/nemotron-3-super-120b-a12b)
```

---

## 上传后的三个检查

- [ ] 可见性是 **Public**（去视频页面确认，不是"不公开"）
- [ ] 时长 **< 3 分钟**（你的是 81 秒）
- [ ] **≥ 1 分钟**是真实模块动作（你的是实拍仿真画面，不是静态图）

然后把链接填到两个地方：
1. **Devpost 表单**的 Video 字段
2. **README.md** 顶部（我之前把它改成了指向仓库内的文件，
   因为你的 YouTube 链接当时还不存在。现在可以换回真链接了——
   你把链接发我，我帮你改并推送）

---

## 常见问题

**Q: 必须出镜吗？**
不必须。规则只要 "footage"，视频里全是仿真画面和文字，完全符合。

**Q: 会被判定为"没有物理硬件"吗？**
规则原文：*"if your Project has no physical hardware component — the key
application modules in action"*。你属于这一类，所以**展示关键模块动作即可**，
这正是 `submission.mp4` 在做的事。

**Q: 要不要配乐？**
不要。规则明确禁止 *"copyrighted music or other material unless the Entrant
has permission"*。不放音乐最安全。

**Q: 如果解说词念不完？**
跳过 ④⑤ 的解说，只念 ①②③ 即可。规则不要求旁白完整。