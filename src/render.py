"""Framebuffer rendering, with no pygame dependency.

The renderer draws into a plain numpy RGB array. That matters for two
reasons:

1. The GIF recorder works with nothing but numpy and Pillow, so a judge
   who clones this repository can reproduce the video without installing a
   windowing library.
2. The web demo (app.py) can hand the same frames to Gradio, so the demo
   and the video show exactly the same picture.

``src/viewer.py`` keeps the interactive pygame window on top of this: it
imports the same drawing code, so the window and the GIF cannot drift
apart.
"""

import numpy as np

from src.grid import cell_to_world

# The same palette as src/viewer.py.
BG = (248, 248, 245)
WALL = (48, 54, 66)
LINE = (208, 208, 202)
PATH_C = (96, 140, 220)
TRAIL = (226, 84, 72)
ROBOT = (58, 168, 96)
ROBOT_EDGE = (255, 255, 255)
START_C = (150, 150, 145)
GOAL_C = (240, 186, 60)

CELL = 44            # pixels per cell
MARGIN = 22          # border margin
FPS = 60             # playback frame rate


def canvas_size(grid, cell=CELL, margin=MARGIN):
    side = margin * 2 + grid.size * cell
    return (side, side)


def _to_px(x, y, grid, cell=CELL, margin=MARGIN):
    """World position (in cells) -> pixel coordinates. y is flipped: the
    world points up, the image points down."""
    return (int(margin + x * cell), int(margin + (grid.size - y) * cell))


# Public alias with the name the rest of the project has always used.
def world_to_screen(x, y, grid, cell=CELL, margin=MARGIN):
    return _to_px(x, y, grid, cell, margin)


def _disc(img, cx, cy, r, color):
    y0, y1 = max(0, cy - r), min(img.shape[0], cy + r + 1)
    x0, x1 = max(0, cx - r), min(img.shape[1], cx + r + 1)
    if y0 >= y1 or x0 >= x1:
        return
    ys = np.arange(y0, y1).reshape(-1, 1)
    xs = np.arange(x0, x1).reshape(1, -1)
    mask = (ys - cy) ** 2 + (xs - cx) ** 2 <= r * r
    img[y0:y1, x0:x1][mask] = color


def _ring(img, cx, cy, r, color, width=2):
    """An outline only -- the disc's interior is left untouched."""
    y0, y1 = max(0, cy - r - width), min(img.shape[0], cy + r + width + 1)
    x0, x1 = max(0, cx - r - width), min(img.shape[1], cx + r + width + 1)
    if y0 >= y1 or x0 >= x1:
        return
    ys = np.arange(y0, y1).reshape(-1, 1)
    xs = np.arange(x0, x1).reshape(1, -1)
    d2 = (ys - cy) ** 2 + (xs - cx) ** 2
    mask = (d2 <= (r + width) ** 2) & (d2 >= (r - width) ** 2)
    img[y0:y1, x0:x1][mask] = color


def _segment(img, p0, p1, color, width):
    """Draw a thick line between two pixel points."""
    x0, y0 = p0
    x1, y1 = p1
    steps = int(max(abs(x1 - x0), abs(y1 - y0))) + 1
    half = width // 2
    for s in range(steps + 1):
        px = int(x0 + (x1 - x0) * s / steps)
        py = int(y0 + (y1 - y0) * s / steps)
        img[max(0, py - half):py + half + 1,
            max(0, px - half):px + half + 1] = color


def render(world, k=None, cell=CELL, margin=MARGIN):
    """Render one frame of a run as an (H, W, 3) uint8 RGB array.

    ``k`` is the number of trajectory samples to show; ``None`` means the
    whole run.
    """
    grid = world["grid"]
    size = grid.size
    side = margin * 2 + size * cell
    img = np.zeros((side, side, 3), dtype=np.uint8)
    img[:, :] = BG

    # Floor tiles.
    for r in range(size):
        for c in range(size):
            x0, y0 = _to_px(c, r + 1, grid, cell, margin)
            if grid.is_wall(r, c):
                img[y0:y0 + cell, x0:x0 + cell] = WALL
            else:
                img[y0:y0 + cell, x0:x0 + cell] = LINE

    # The planned path.
    pts = [_to_px(*cell_to_world(c), grid, cell, margin) for c in world["path"]]
    for a, b in zip(pts[:-1], pts[1:]):
        _segment(img, a, b, PATH_C, 4)

    # The trajectory driven so far.
    traj = world["traj"]
    if k is not None:
        traj = traj[:k]
    if len(traj) > 1:
        walked = [_to_px(x, y, grid, cell, margin) for x, y in traj]
        for a, b in zip(walked[:-1], walked[1:]):
            _segment(img, a, b, TRAIL, 2)

    # Start and goal markers. The goal is a filled disc with an outline
    # drawn around it, so the fill stays visible.
    _disc(img, *_to_px(*cell_to_world(world["start"]), grid, cell, margin), 6, START_C)
    gx, gy = _to_px(*cell_to_world(world["goal"]), grid, cell, margin)
    _disc(img, gx, gy, 8, GOAL_C)
    _ring(img, gx, gy, 9, WALL, 2)

    # The robot, with a short heading tick.
    if traj:
        idx = len(traj) - 1
        x, y = traj[idx]
        theta = world["thetas"][idx]
        rx, ry = _to_px(x, y, grid, cell, margin)
        tip = _to_px(x + 0.30 * np.cos(theta), y + 0.30 * np.sin(theta),
                     grid, cell, margin)
        _segment(img, (rx, ry), tip, ROBOT_EDGE, 2)
        _disc(img, rx, ry, 7, ROBOT)
        _ring(img, rx, ry, 7, ROBOT_EDGE, 2)

    # Progress bar along the bottom: how far along the run we are.
    n = len(world["traj"])
    if n > 1 and k:
        bar_w = side - 2 * margin
        bar_y = side - margin // 2 - 3
        img[bar_y:bar_y + 6, margin:margin + bar_w] = LINE
        img[bar_y:bar_y + 6, margin:margin + int(bar_w * k / n)] = ROBOT

    return img


def record_gif(world, out_path, every=3, size=480, colors=128, fps=60):
    """Record the run to a GIF without opening a window.

    Requires only numpy and Pillow. Returns (number of frames, size in
    bytes).
    """
    import os

    from PIL import Image

    n_traj = len(world["traj"])
    frame_ms = int(round(1000 / fps * every))

    frames = []
    for k in range(1, n_traj + 1):
        if (k - 1) % every:
            continue
        img = Image.fromarray(render(world, k)).convert("RGB")
        img = img.resize((size, size), Image.LANCZOS)
        frames.append(img.quantize(colors=colors))

    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    frames[0].save(out_path, save_all=True, append_images=frames[1:],
                   duration=frame_ms, loop=0, optimize=True)
    return len(frames), os.path.getsize(out_path)
