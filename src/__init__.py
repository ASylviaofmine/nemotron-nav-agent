"""A* grid path planning + go-to-goal tracking, written from scratch.

This is the *classical* half of the project: no learning, no model calls.
The path planner is A* with a Manhattan heuristic on a 4-connected grid;
the tracker is a proportional heading controller that drives the robot along
the planned waypoints.

The other half -- the part where an NVIDIA Nemotron model supervises this
loop -- lives in ``src/agent.py`` and ``src/nebius_client.py``.

Module layout (dependencies point one way only):

    grid  <-  planner  <-  simulation  ->  render  ->  viewer
                          ^
                       metrics
                          ^
                        agent  ->  nebius_client
"""

from src.grid import Grid, cell_to_world, world_to_cell
from src.planner import astar, path_steps
from src.controller import follow, wrap_angle, path_length, end_point_error

__all__ = [
    "Grid", "cell_to_world", "world_to_cell",
    "astar", "path_steps",
    "follow", "wrap_angle", "path_length", "end_point_error",
]
