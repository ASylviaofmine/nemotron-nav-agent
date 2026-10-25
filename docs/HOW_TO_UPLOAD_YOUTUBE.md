# YouTube 上传 — 逐步照着做

**要传的文件**（选这个，不要选剪映导出的那个）：

```
C:\Users\Lee\WorkBuddy\2026-10-21-22-18-37\nemotron-nav-agent\docs\submission-subtitled.mp4
```

| | 这个文件 | 剪映导出的 `nvida video.mp4` |
|---|---|---|
| 比例 | **1.4286 精确** | 1.3925（压扁 2.5%） |
| 黑边 | **无** | 右侧 59px + 顶部 15px |
| 音频 | **无音轨** | 有音轨（可能是版权音乐） |
| 大小 | 8.7 MB | 9.16 MB |

---

## 第 1 步：打开上传页

**https://studio.youtube.com**（会自动跳转到 `studio.youtube.com/channel/.../videos/upload`）

如果没登录会先跳 Google 账号登录，用你的账号进。

---

## 第 2 步：拖文件

页面中央有一个虚线框，写着 *"Drag and drop video files here"*。

把 `submission-subtitled.mp4` **直接拖进去**。

上传会立刻开始（8.7 MB，家宽几秒到几十秒），进度条走完就进下一步。

---

## 第 3 步：填标题和描述

这一步是**唯一需要打字**的地方。

### Title（标题框）

```
nemotron-nav-agent — a Nemotron model supervises a robot's tracking controller
```

（86 字符，YouTube 上限 100）

### Description（描述框）

**粘贴下面这一整段**（在 `docs/VIDEO_SCRIPT.md` 末尾也有）：

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

> **注意缩进**：最后那几行命令前面有 **4 个空格**，这样 YouTube 会渲染成
> 代码块。粘贴时会保留。

---

## 第 4 步：缩略图

YouTube 会自动给你三张候选帧让你选，标着 *"Video content"* 和三个时间点。

**选中间那张**（大约 40 秒的位置）——那正是"基线 vs 调优 + 两条实时误差曲线"
的对比画面，红线 0.0895 m、绿线 0.0233 m。**这是整段视频最该被看到的一幕。**

如果想更准，可以上传自定义缩略图：

```
C:\Users\Lee\WorkBuddy\2026-10-21-22-18-37\nemotron-nav-agent\docs\thumbnail.png
```

（1000×700，就是那张对比图）

---

## 第 5 步：⚠️ Visibility —— 这一步最容易出错

**点 Next 之后，最后一步就是可见性。**

YouTube 的默认值是 **Private**（私密）。**选 Private 等于白传。**

点 **Visibility** 下拉，选：

| 选项 | 行不行 |
|---|---|
| **Public**（公开） | ✅ **选这个** |
| Unlisted（不公开） | ⚠️ 规则技术上允许，但评委点链接可能打不开 |
| Private（私密） | ❌ **绝对不行** |

---

## 第 6 步：发布

点 **Publish**。

等 30 秒到几分钟，YouTube 需要处理转码和缩略图。

---

## 第 7 步：验证（别跳过）

1. 复制视频链接（发布后在 **Content** 列表里点视频标题，或点"分享"复制链接）
2. **开一个无痕窗口**（Ctrl + Shift + N）打开这个链接
3. 确认：
   - ✅ 能播放
   - ✅ 时长显示 **1:21**（81 秒）
   - ✅ 右下角没有"Private"字样

如果无痕窗口打不开 → 说明还是 Private，回 Studio 改。

---

## 第 8 步：填到两个地方

### ① Devpost 表单

- **Demo video URL** 字段 → 粘贴链接
- 这个字段在 "Project details" 页，是**必填**

### ② README

把链接发我，我改好 README 顶部并推送。

（现在那里指向仓库内的 `docs/submission.mp4`，因为你的 YouTube 链接
当时还不存在。）

---

## 常见问题

**Q: 上传后 YouTube 显示"Processing"很久？**
正常。8.7 MB 的 1080p 以下视频通常 30 秒到几分钟。

**Q: 需要等处理完才能填表单吗？**
不用。链接一旦生成就能填，视频会自己处理完。

**Q: 视频没有声音会有问题吗？**
不会。规则没要求音频，评委看的是画面。

**Q: 会被判定为"没有物理硬件所以不合格"吗？**
不会。规则原文针对无硬件项目写的是
*"or — if your project has no physical hardware component — the key
application modules in action"*。你的视频正是在展示关键模块在动。

**Q: 视频里只有画面没有解说，会不会太单薄？**
不会。视频里每幕都有标题和数值，而且有英文字幕。

**Q: 标题里带 em dash "—" 有问题吗？**
没有，YouTube 支持 UTF-8。

**Q: 如果上传后发现文件不对？**
在 Studio 里点视频 → 详情 → 替换视频，重新拖 `submission-subtitled.mp4`。

**Q: 能不能同时传两个视频？**
可以，但**没必要**。规则看的是你填的那个链接，传两个只会让评委困惑。
