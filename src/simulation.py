"""Wires map, planning and control into "one complete run".

A caller only has to remember one thing:

    world = build_world()
    world["traj"]   # the path the robot actually drove

The returned world is a dictionary; the renderer, the reports and the
benchmark all take their data from it -- so the modules exchange "the
result of one run" instead of a pile of loose parameters.
"""

from src.grid import Grid, cell_to_world
from src.planner import astar
from src.controller import follow

DEFAULT_SIZE = 10
DEFAULT_START = (1, 1)
DEFAULT_GOAL = (8, 8)


def make_map(size=DEFAULT_SIZE, wall_row=None):
    """Build the canonical test map: one horizontal wall across the middle
    with a gap at each end, forcing the planner to detour.

    At 10 x 10: row 5, columns 1..8 are wall; (5,0) and (5,9) are the only
    two openings.
    """
    grid = Grid(size)
    row = size // 2 if wall_row is None else wall_row
    for c in range(1, size - 1):
        grid.set_wall(row, c)
    return grid


def build_world(size=DEFAULT_SIZE, start=DEFAULT_START, goal=DEFAULT_GOAL, **ctrl):
    """Map -> A* plan -> waypoint tracking. Returns everything about the run.

    Keyword arguments in ``ctrl`` are passed straight through to
    ``controller.follow()``, so ``build_world(tol=0.2, Kp=8)`` is a valid
    parameter experiment.
    """
    grid = make_map(size)
    path = astar(grid, start, goal)
    if path is None:
        raise ValueError(f"goal {goal} is unreachable from {start} on this map")

    waypoints = [cell_to_world(cell) for cell in path]
    traj, thetas, t = follow(waypoints, **ctrl)

    return {
        "grid": grid,
        "start": start,
        "goal": goal,
        "path": path,
        "waypoints": waypoints,
        "traj": traj,
        "thetas": thetas,
        "time": t,
    }


def describe(world):
    """Reduce one run to a one-line summary for quick terminal checking."""
    return (f"path {len(world['path'])} cells / {len(world['path']) - 1} steps, "
            f"trajectory {len(world['traj'])} samples, "
            f"time {world['time']:.2f} s")
