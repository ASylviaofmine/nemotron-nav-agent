"""Trajectory metrics for one run.

``tools/benchmark_ref.py`` holds an equivalent standalone implementation
(a self-contained copy, so it can be run on its own). This module lifts the
same definitions into a reusable module so that the agent and the benchmark
share one set of definitions -- two disagreeing definitions of "error" is
the easiest mistake to make in a project like this.

The one that matters most: **cross-track error is the distance to the
planned polyline, not the distance to the nearest waypoint.** With waypoints
one metre apart, a robot tracking the path perfectly is still up to 0.5 m
from the nearest waypoint, so the wrong definition yields a constant that
looks like the grid spacing and hides the effect of every parameter.
"""

import numpy as np


def dist_point_to_segment(p, a, b):
    """Shortest distance from a point to a segment.

    The perpendicular foot may fall outside the segment, in which case the
    closest point is an endpoint. Clamping the projection parameter t to
    [0, 1] handles both cases at once.
    """
    ab = b - a
    L2 = ab @ ab
    if L2 < 1e-12:                                    # degenerate: a == b
        return float(np.hypot(*(p - a)))
    t = np.clip((p - a) @ ab / L2, 0.0, 1.0)
    proj = a + t * ab
    return float(np.hypot(*(p - proj)))


def crosstrack_error(traj, waypoints):
    """Distance from every trajectory sample to the planned polyline.

    Vectorised: all (sample, segment) distances are computed in one pass
    and reduced with a row-wise minimum. Numerically identical to the
    per-point loop (``tools/selftest.py`` checks this bit for bit), but
    about two orders of magnitude faster -- the exhaustive parameter sweep
    runs hundreds of simulations.
    """
    P = np.array(traj, dtype=float)
    W = np.array(waypoints, dtype=float)
    A, B = W[:-1], W[1:]                      # (S, 2)

    ab = B - A                                # (S, 2)
    L2 = np.sum(ab * ab, axis=1)              # (S,)
    L2_safe = np.where(L2 < 1e-12, 1.0, L2)  # degenerate segments handled apart

    # (N, S): every sample relative to every segment
    AP = P[:, None, :] - A[None, :, :]        # (N, S, 2)
    t = np.sum(AP * ab[None, :, :], axis=2) / L2_safe[None, :]
    t = np.clip(t, 0.0, 1.0)
    proj = A[None, :, :] + t[:, :, None] * ab[None, :, :]
    d = np.hypot(P[:, None, 0] - proj[:, :, 0], P[:, None, 1] - proj[:, :, 1])

    # Degenerate segment (a == b): the distance is the distance to the endpoint
    degenerate = L2 < 1e-12
    if np.any(degenerate):
        d[:, degenerate] = np.hypot(
            P[:, None, 0] - A[None, degenerate, 0],
            P[:, None, 1] - A[None, degenerate, 1],
        )

    return np.min(d, axis=1)


def path_length(traj):
    """Distance actually travelled."""
    pts = np.array(traj, dtype=float)
    return float(np.sum(np.hypot(np.diff(pts[:, 0]), np.diff(pts[:, 1]))))


def end_point_error(traj, goal_xy):
    """How far the final position still is from the goal point."""
    return float(np.hypot(traj[-1][0] - goal_xy[0], traj[-1][1] - goal_xy[1]))


def measure(world):
    """Reduce a full run to a set of metrics.

    Input is the world dictionary returned by ``src.simulation.build_world()``.
    Output is a plain dictionary of numbers -- this is exactly what is fed
    to Nemotron.
    """
    traj = world["traj"]
    waypoints = world["waypoints"]
    goal_xy = waypoints[-1]

    ct = crosstrack_error(traj, waypoints)
    return {
        "time_s": round(float(world["time"]), 3),
        "distance_m": round(path_length(traj), 3),
        "end_point_error_m": round(end_point_error(traj, goal_xy), 4),
        "max_cross_track_m": round(float(ct.max()), 4),
        "mean_cross_track_m": round(float(ct.mean()), 4),
        "path_cells": len(world["path"]),
        "path_steps": len(world["path"]) - 1,
        "samples": len(traj),
    }


def measure_world(traj, waypoints, t, path_cells):
    """For the cases where building a full world is inconvenient
    (e.g. the agent re-running inside its loop)."""
    ct = crosstrack_error(traj, waypoints)
    return {
        "time_s": round(float(t), 3),
        "distance_m": round(path_length(traj), 3),
        "end_point_error_m": round(end_point_error(traj, waypoints[-1]), 4),
        "max_cross_track_m": round(float(ct.max()), 4),
        "mean_cross_track_m": round(float(ct.mean()), 4),
        "path_cells": path_cells,
        "path_steps": path_cells - 1,
        "samples": len(traj),
    }


def format_metrics(m):
    """The metric text shown to the model. Keep full precision -- do not
    round these to integers."""
    return (
        f"- time to goal: {m['time_s']:.2f} s\n"
        f"- distance travelled: {m['distance_m']:.2f} m\n"
        f"- end-point error: {m['end_point_error_m']:.3f} m\n"
        f"- max cross-track error: {m['max_cross_track_m']:.4f} m\n"
        f"- mean cross-track error: {m['mean_cross_track_m']:.4f} m\n"
        f"- planned path: {m['path_steps']} steps"
    )
