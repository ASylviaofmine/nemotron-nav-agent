"""Burn English subtitles into the submission video, from the original frames.

The CapCut export is fine as far as the subtitles go -- they are legible
and they do not cover anything -- but the export dialog's 1080P preset
is a 16:9 canvas, and the footage is 1.4286. So the picture ends up
slightly squashed inside a canvas with a black strip down the right
edge. Re-encoding from the original frames fixes that: the aspect ratio
is exactly right and there is no black bar at all.

The subtitles are the ones already written in docs/VIDEO_SCRIPT.md,
placed in the empty band below the simulation panels, which is blank in
the original frames. The last line of the video carries its own closing
sentence, so the subtitle for that moment is left out rather than
doubled up.

    python tools/make_subtitled.py
"""

import os
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "docs", "submission.mp4")
OUT = os.path.join(ROOT, "docs", "submission-subtitled.mp4")

W, H = 1000, 700
FPS = 20

# The subtitles sit in the band below the simulation panels, which the
# original frames leave empty. The band starts below y=630: the A* scene
# prints "5 of 17 cells found" at y=613 and the generalisation scene
# draws its bars down to y=605, so 632 is clear of both.
SUB_TOP = 632
SUB_BOTTOM = 690

_FONTS = {}


def font(size):
    """A serif face that exists on Windows, cached.

    The font is loaded once and reused: loading a TTF on every frame
    takes minutes over a whole video.
    """
    if size not in _FONTS:
        loaded = None
        for name in ("times.ttf", "timesbd.ttf", "georgia.ttf", "segoeui.ttf"):
            try:
                loaded = ImageFont.truetype(name, size)
                break
            except OSError:
                continue
        _FONTS[size] = loaded or ImageFont.load_default()
    return _FONTS[size]


# (start, end, text). The timings are seconds in the original video.
#
# The opening line is deliberately not repeated here: the title card
# already says it, on screen, for the first six seconds. Saying it twice
# wastes the only moment where the viewer is deciding whether to keep
# watching.
SUBS = [
    (6.5, 10.5, "First, A* finds the route around the wall."),
    (11.0, 15.0, "Then the robot follows it with a proportional heading controller."),
    (18.0, 22.0, "This is the core of the project: the same task, tracked twice."),
    (22.0, 26.0, "Left: the baseline parameters. Right: the parameters the model chose."),
    (26.5, 30.5, "The plot under each panel is the measured cross-track error."),
    (30.5, 34.5, "The red curve climbs to five centimetres and keeps oscillating."),
    (34.5, 38.0, "The green one stays near the floor."),
    (38.0, 42.0, "And the tuned run finishes slightly faster."),
    (42.0, 46.0, "Better tracking, and lower cost."),
    (52.5, 56.0, "Does it generalise? The same loop over a seeded suite of maps."),
    (56.0, 60.0, "Every bar pair is one map. It improves on all of them."),
    (63.5, 67.0, "What the model actually says."),
    (64.0, 69.0, "Cross-track error dominates the residual; the gain is too low."),
    (69.0, 72.5, "It proposes raising Kp from five to twelve."),
    (73.5, 77.0, "That is a hypothesis, not a result."),
    (75.0, 78.5, "The simulator re-runs, and the measurement decides."),
]


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap, so a long line becomes two short ones."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_subtitles(img, t):
    """Draw whichever subtitle belongs to time t onto the frame.

    A solid bar across the bottom separates the subtitle from whatever
    the video itself is printing there. The A* scene writes "the robot
    follows it (t = 20.7 s)" at y=618, and without the bar the two
    would read as one line -- which is exactly what happened in the
    first attempt.
    """
    for start, end, text in SUBS:
        if not (start <= t < end):
            continue
        draw = ImageDraw.Draw(img)
        fnt = font(19)
        lines = wrap(draw, text, fnt, W - 120)

        band_h = 34 * len(lines) + 16
        band_top = H - band_h
        draw.rectangle([0, band_top, W, H], fill=(252, 252, 250))
        draw.line([(0, band_top), (W, band_top)], fill=(214, 214, 208))

        y = band_top + 8
        for line in lines:
            x = (W - draw.textlength(line, font=fnt)) / 2
            draw.text((x, y), line, font=fnt, fill=(30, 32, 38))
            y += 24
        break


def main():
    if not os.path.exists(SRC):
        print(f"missing {SRC} -- run tools/make_demo.py first", file=sys.stderr)
        return 1

    cap = cv2.VideoCapture(SRC)
    if not cap.isOpened():
        print(f"cannot open {SRC}", file=sys.stderr)
        return 1

    n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(OUT, fourcc, FPS, (W, H))

    for i in range(n):
        ok, frame = cap.read()
        if not ok:
            break
        img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        draw_subtitles(img, i / FPS)
        out.write(cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR))

    out.release()
    cap.release()
    size = os.path.getsize(OUT) / 1024 / 1024
    print(f"{OUT}\n  {n} frames, {n / FPS:.0f} s, {W}x{H}, {size:.1f} MB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
