"""Interactive pygame viewer, plus GIF recording.

Two public functions:
    play(world)        open a pygame window and play the run frame by frame
                      (press R to replay, close the window to quit)
    record_gif(world)  record the run to a GIF

The drawing itself lives in ``src/render.py``, which is dependency-light
and shared with the web demo -- so the window, the GIF and the demo can
never show different pictures.

pygame is imported lazily inside ``play``, so ``record_gif`` and the rest
of the project work on a machine where pygame is not installed.
"""

import os

# Silence pygame's first-run greeting (the line with a pygame.org link)
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

from src.grid import cell_to_world
from src.render import BG, CELL, FPS, GOAL_C, LINE, MARGIN, PATH_C, ROBOT, \
    ROBOT_EDGE, START_C, TRAIL, WALL, canvas_size, record_gif, render, world_to_screen

__all__ = ["play", "record_gif", "canvas_size", "render", "world_to_screen",
           "CELL", "MARGIN", "FPS", "BG", "WALL", "LINE", "PATH_C", "TRAIL",
           "ROBOT", "ROBOT_EDGE", "START_C", "GOAL_C"]


def play(world, fps=FPS):
    """Play one run in a live window. Press R to replay, close to quit."""
    import math

    import pygame

    pygame.init()
    screen = pygame.display.set_mode(canvas_size(world["grid"]))
    pygame.display.set_caption("nemotron-nav-agent - A* planning + go-to-goal tracking")
    clock = pygame.time.Clock()

    grid = world["grid"]

    def draw(surface, k):
        """Blit the numpy renderer's frame onto a pygame surface."""
        # The renderer is the single source of truth; the window just shows it.
        import numpy as np
        arr = render(world, k)
        surface.fill(BG)
        surface.blit(pygame.image.frombuffer(arr.tobytes(), arr.shape[1::-1], "RGB"), (0, 0))
        return surface

    k, running = 1, True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                k = 1

        if k < len(world["traj"]):
            k = k + 1

        draw(screen, k)
        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()
