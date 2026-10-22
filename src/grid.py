"""Grid map and coordinate conversion.

A map is a size x size array: 0 = free, 1 = wall.
Row index r grows downward (world y grows upward), column index c grows
to the right (world x grows rightward). One cell = 1 metre, and the world
position of cell (r, c) is its centre (c + 0.5, r + 0.5).
"""

import numpy as np


class Grid:
    """A square occupancy grid. Out-of-bounds counts as wall, so the
    planner needs no separate boundary checks."""

    FREE = 0
    WALL = 1

    def __init__(self, size):
        self.size = size
        self.cells = np.zeros((size, size), dtype=int)

    def set_wall(self, row, col):
        self.cells[row, col] = self.WALL

    def in_bounds(self, row, col):
        return 0 <= row < self.size and 0 <= col < self.size

    def is_wall(self, row, col):
        """Out of bounds = wall. This single rule keeps the planner's
        neighbour check down to one line."""
        if not self.in_bounds(row, col):
            return True
        return self.cells[row, col] == self.WALL

    def wall_count(self):
        return int(self.cells.sum())

    def __repr__(self):
        return f"Grid(size={self.size}, walls={self.wall_count()})"


def cell_to_world(cell):
    """Grid cell (row, col) -> world position (x, y), at the cell centre.

    Note the order is reversed: the column sets x, the row sets y.
    (1, 1) -> (1.5, 1.5);  (5, 0) -> (0.5, 5.5)
    """
    r, c = cell
    return (c + 0.5, r + 0.5)


def world_to_cell(x, y):
    """World position (x, y) -> the cell (row, col) containing it.
    The inverse of ``cell_to_world``."""
    return (int(np.floor(y)), int(np.floor(x)))
