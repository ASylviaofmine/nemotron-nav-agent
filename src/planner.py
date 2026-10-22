"""A* grid path planning (4-connected, unit step cost, Manhattan heuristic).

f(n) = g(n) + h(n)
    g   the real number of steps taken from the start to n
    h   the estimated number of steps still to go (Manhattan distance)
As long as h never overestimates, A* returns a shortest path.

Why Manhattan and not Euclidean: the robot can only move up, down, left
or right, and each step costs exactly 1 -- diagonals do not exist. The
Manhattan distance is precisely "how many steps remain in the best case
without hitting a wall", i.e. the tightest admissible heuristic on a
4-connected grid.
"""

from heapq import heappush, heappop


def heuristic(a, b):
    """Manhattan distance |dr| + |dc|."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar(grid, start, goal):
    """Shortest cell path from start to goal on ``grid``.

    Returns [(r, c), ...] including both endpoints, or None if the goal
    is unreachable. The caller must handle None -- a walled-in goal
    neither raises nor loops forever.
    """
    open_list = []
    heappush(open_list, (0, start))
    came_from = {}
    g = {start: 0}
    visited = set()

    while open_list:
        f, cur = heappop(open_list)

        if cur == goal:
            path = [cur]
            while cur in came_from:
                cur = came_from[cur]
                path.append(cur)
            return path[::-1]

        if cur in visited:
            continue
        visited.add(cur)

        r, c = cur
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nb = (r + dr, c + dc)
            if grid.is_wall(nb[0], nb[1]):
                continue
            ng = g[cur] + 1
            if nb not in g or ng < g[nb]:
                g[nb] = ng
                came_from[nb] = cur
                heappush(open_list, (ng + heuristic(nb, goal), nb))

    return None


def path_steps(path):
    """How many steps the path takes (number of cells = steps + 1)."""
    return len(path) - 1
