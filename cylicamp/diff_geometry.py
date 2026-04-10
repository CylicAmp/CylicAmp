"""
A Down-to-Earth Introduction to Differential Geometry

Differential geometry studies curved spaces using calculus.
Instead of flat grids, it works with surfaces, curves, and shapes
that bend and twist through space.

Key ideas, explained plainly:
- A curve is a path through space
- A surface is a 2D shape living in 3D space
- Curvature measures how much something bends
- A tangent is the direction something is heading at any point
- A normal is the direction pointing straight out from a surface
"""

import math
from typing import Tuple, List


# --- CURVES ---

def parametric_curve(t: float) -> Tuple[float, float, float]:
    """
    A simple 3D curve parameterized by t.
    As t changes, the point moves along the curve.
    This one is a helix — like a spring or a spiral staircase.
    """
    x = math.cos(t)
    y = math.sin(t)
    z = t / (2 * math.pi)
    return (x, y, z)


def tangent_vector(t: float, dt: float = 1e-6) -> Tuple[float, float, float]:
    """
    The tangent vector at point t — the direction the curve is heading.
    Computed by taking a tiny step forward and measuring the difference.
    """
    p1 = parametric_curve(t)
    p2 = parametric_curve(t + dt)
    return (
        (p2[0] - p1[0]) / dt,
        (p2[1] - p1[1]) / dt,
        (p2[2] - p1[2]) / dt,
    )


def curvature(t: float, dt: float = 1e-6) -> float:
    """
    Curvature measures how sharply a curve bends at point t.
    A straight line has curvature 0. A tight circle has high curvature.
    """
    t1 = tangent_vector(t, dt)
    t2 = tangent_vector(t + dt, dt)
    diff = (
        (t2[0] - t1[0]) / dt,
        (t2[1] - t1[1]) / dt,
        (t2[2] - t1[2]) / dt,
    )
    return math.sqrt(diff[0]**2 + diff[1]**2 + diff[2]**2)


# --- SURFACES ---

def sphere_point(phi: float, theta: float, radius: float = 1.0) -> Tuple[float, float, float]:
    """
    A point on a sphere, given two angles:
    phi = angle from the north pole (0 to pi)
    theta = angle around the equator (0 to 2*pi)
    """
    x = radius * math.sin(phi) * math.cos(theta)
    y = radius * math.sin(phi) * math.sin(theta)
    z = radius * math.cos(phi)
    return (x, y, z)


def gaussian_curvature_sphere(radius: float) -> float:
    """
    Gaussian curvature of a sphere is 1/r^2.
    A flat plane has curvature 0. A sphere always curves the same amount everywhere.
    """
    return 1.0 / (radius ** 2)


# --- GEODESICS ---

def great_circle_distance(
    lat1: float, lon1: float,
    lat2: float, lon2: float,
    radius: float = 1.0
) -> float:
    """
    The shortest path between two points on a sphere is called a geodesic.
    On Earth, this is a great circle route — what airplanes actually fly.

    Inputs are in radians.
    """
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2)
    return radius * 2 * math.asin(math.sqrt(a))


# --- DEMO ---

def run_intro() -> None:
    print("\n=== A Down-to-Earth Introduction to Differential Geometry ===\n")

    print("1. CURVES")
    print("   A helix at t=0:", parametric_curve(0))
    print("   A helix at t=pi:", tuple(round(v, 4) for v in parametric_curve(math.pi)))
    print("   Tangent at t=0:", tuple(round(v, 4) for v in tangent_vector(0)))
    print("   Curvature at t=0:", round(curvature(0), 4))
    print()

    print("2. SURFACES")
    print("   Point on unit sphere (phi=pi/4, theta=pi/4):",
          tuple(round(v, 4) for v in sphere_point(math.pi/4, math.pi/4)))
    print("   Gaussian curvature of unit sphere:", gaussian_curvature_sphere(1.0))
    print()

    print("3. GEODESICS")
    dist = great_circle_distance(0, 0, math.pi/2, 0)
    print(f"   Shortest path from equator to north pole: {round(dist, 4)} radians")
    print(f"   On Earth (radius 6371km): {round(dist * 6371, 1)} km")
    print()


if __name__ == "__main__":
    run_intro()
