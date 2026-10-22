"""Waypoint tracking controller: proportional go-to-goal steering with
angle wrapping.

This module deliberately knows nothing about ``Grid`` -- it only receives a
list of (x, y) waypoints. The upside is that the same controller can track
a grid path or a hand-drawn curve.

Each step does three things:
    1. work out which way the target lies  theta_target = arctan2(dy, dx)
    2. work out how far off the heading is e = theta_target - theta, wrapped into (-pi, pi]
    3. turn the heading, then move forward along it
"""

import numpy as np

# Default parameters, tuned on the canonical map.
DEFAULT_TOL = 0.05        # metres: how close counts as "caught the waypoint"
DEFAULT_SPEED = 0.5       # forward speed, metres per second
DEFAULT_KP = 5.0          # steering gain
DEFAULT_DT = 0.05         # simulation step, seconds


def wrap_angle(e):
    """Fold an angle difference into (-pi, pi] so the robot always turns
    the short way round.

    Without this, theta accumulates into the tens of radians, the error
    explodes with it, and the robot spins on the spot without ever
    converging on its target.
    """
    return (e + np.pi) % (2 * np.pi) - np.pi


def follow(waypoints, tol=DEFAULT_TOL, speed=DEFAULT_SPEED,
           Kp=DEFAULT_KP, dt=DEFAULT_DT, t_max=200.0):
    """Drive along the waypoints. Returns (trajectory, headings, duration).

    The trajectory is [(x, y), ...] with length = number of steps + 1;
    thetas[i] is the heading after step i, which the renderer needs in
    order to draw the robot's orientation.

    ``t_max`` is a safety valve: if the waypoint list is wrong, the
    simulation stops after this many seconds instead of looping forever.
    """
    x, y, theta = waypoints[0][0], waypoints[0][1], 0.0
    idx, t = 1, 0.0
    traj, thetas = [(x, y)], [theta]

    while idx < len(waypoints) and t < t_max:
        tx, ty = waypoints[idx]

        theta_target = np.arctan2(ty - y, tx - x)
        e = wrap_angle(theta_target - theta)
        theta = theta + Kp * e * dt

        x = x + speed * np.cos(theta) * dt
        y = y + speed * np.sin(theta) * dt
        t = t + dt

        traj.append((x, y))
        thetas.append(theta)

        if np.hypot(tx - x, ty - y) < tol:
            idx = idx + 1

    return traj, thetas, t


def path_length(traj):
    """Distance actually travelled (the sum of the straight segments)."""
    return float(np.sum(np.hypot(np.diff([p[0] for p in traj]),
                                 np.diff([p[1] for p in traj]))))


def end_point_error(traj, goal_xy):
    """How far the final position still is from the goal point."""
    return float(np.hypot(traj[-1][0] - goal_xy[0], traj[-1][1] - goal_xy[1]))
