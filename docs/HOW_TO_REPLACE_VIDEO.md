# 替换 YouTube 视频 —— 一步步

## 为什么要换

你上传的是剪映导出的 `nvida video.mp4`，有两个问题：

| | 剪映版（已上传） | 字幕版（要用这个） |
|---|---|---|
| 画面比例 | 1.4278（画布），内容被压扁 2.5% | **1.4286 精确** |
| 黑边 | 右侧 59px + 顶部 15px | **无** |
| 音频 | 有 → **YouTube 生成了自动字幕** | **无音轨** |
| 字幕层数 | 烧录的 + YouTube 自动字幕 = **两层重叠** | **只有一层** |

**"两层字幕重叠"是怎么来的**：剪映版有音轨，YouTube 就自动生成了一条字幕轨道。
视频画面里又已经烧录了字幕，于是 Devpost 的播放器上同时显示两条——
截图里那两行交错的字就是。

字幕版**没有音轨**，YouTube 不会生成自动字幕，只剩一层，不会重叠。

---

## ⚠️ 先记住一件事：链接会变

替换视频后，**YouTube 视频 ID 会变**（新的 URL）。

所以替换完成后：
1. 去 Devpost 的 **Edit hackathon submission** → 把新的 Video URL 改掉
2. 把新链接发我，我改 README

**Devpost 表单可以改**，截图里那个 "Edit hackathon submission" 按钮就是干这个的。
距截止还有 4 天，来得及。

---

## 替换步骤

### ① 打开 YouTube Studio

**https://studio.youtube.com** → 左边 **Content**（内容）→ 找到你的视频

### ② 替换文件

点视频右侧的 **⋮**（三个点）→ **Replace video**（替换视频）

（也可以点视频标题进详情页，在 **Video details** 里找替换选项）

### ③ 拖入新文件

把这个拖进去：

```
C:\Users\Lee\Desktop\nemotron-nav-agent-subtitled.mp4
```

（我已经复制到桌面了。也在
 `C:\Users\Lee\WorkBuddy\2026-10-21-22-18-37\nemotron-nav-agent\docs\submission-subtitled.mp4`）

### ④ ⚠️ 标题和描述要重新填

替换视频**不会保留标题和描述**（有的版本会弹窗问你要不要保留，勾上）。

**标题**：
```
nemotron-nav-agent — a Nemotron model supervises a robot's tracking controller
```

**描述**：复制 `docs/VIDEO_SCRIPT.md` 末尾那段（含仓库链接和复现命令）。

### ⑤ 可见性确认还是 **Public**

### ⑥ Publish

---

## ⑦ 验证字幕不再重叠

发布后打开视频，看第 35-40 秒（"The green one stays near the floor." 那句）。

- ✅ 只显示**一行**字幕，底部有浅色条带
- ❌ 如果还是两行 → 说明 YouTube 又生成了自动字幕

**如果还是两行**，去 YouTube Studio → 左侧 **Subtitles** → 找到那条自动生成的 →
点 **⋮** → **Delete**（删除）。因为字幕已经烧进画面里了，不需要字幕轨道。

---

## ⑧ 改 Devpost 的 Video URL

1. 点截图里那个 **Edit hackathon submission** 按钮
2. 找到 **Demo video URL** 字段
3. 换成**新链接**
4. 保存

> 注意：这个字段在 "Project details" 页，是必填项。

---

## ⑨ 改 README

把新链接发我，我改好 README 顶部并推送。

---

## 或者：不想折腾的话

**Devpost 上现在这个版本已经合规了。** 规则只要求：
- 公开可见 ✓
- 少于 3 分钟 ✓（81 秒）
- 至少 1 分钟展示关键模块动作 ✓

字幕重叠是**观感问题**，不是合规问题。距截止还有 4 天，你可以：
- 现在就换（30 分钟，效果更好）
- 或者先不管，等提交截止后再换（**不推荐**，评审期是 12 月，评委看到的就是这个版本）

**我建议现在换。** 字幕重叠是评委打开视频后**第一眼**就能看到的东西，
而这第一眼决定了他们愿不愿意看完这 81 秒。
