# DIFFERENTIAL GEOMETRY: Curves, Surfaces, Curvature & Geodesics
# ================================================================
# Everything explained in plain language inside the code

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# ================================================================
# PART 1: CURVES - Lines that bend through space
# ================================================================

class Curve:
    """
    A parametric curve in 3D space.

    Think of it like a particle moving through space. At each moment t,
    the particle is at position r(t). The path it traces is the curve.
    """

    def __init__(self, x_func, y_func, z_func, t_range=(-np.pi, np.pi)):
        self.x = x_func
        self.y = y_func
        self.z = z_func
        self.t_min, self.t_max = t_range

    def position(self, t):
        """Where is the particle at time t?"""
        return np.array([self.x(t), self.y(t), self.z(t)])

    def velocity(self, t, dt=1e-6):
        """
        The velocity vector at time t.
        Mathematically: v(t) = dr/dt
        """
        r_plus = self.position(t + dt)
        r_minus = self.position(t - dt)
        return (r_plus - r_minus) / (2 * dt)

    def tangent(self, t):
        """The unit tangent vector - direction of the curve at point t."""
        v = self.velocity(t)
        v_norm = np.linalg.norm(v)
        if v_norm < 1e-10:
            return np.array([0, 0, 0])
        return v / v_norm

    def acceleration(self, t, dt=1e-6):
        """How is the velocity changing? This tells us about curvature."""
        v_plus = self.velocity(t + dt, dt)
        v_minus = self.velocity(t - dt, dt)
        return (v_plus - v_minus) / (2 * dt)

    def curvature(self, t):
        """
        How sharply is the curve bending at point t?
        Curvature = |v x a| / |v|^3
        - Straight line: curvature = 0
        - Tight circle: high curvature
        """
        v = self.velocity(t)
        a = self.acceleration(t)
        v_norm = np.linalg.norm(v)
        if v_norm < 1e-10:
            return 0
        cross = np.cross(v, a)
        return np.linalg.norm(cross) / (v_norm ** 3)

    def normal_vector(self, t):
        """The principal normal vector - points toward center of curvature."""
        v = self.velocity(t)
        a = self.acceleration(t)
        v_norm = np.linalg.norm(v)
        if v_norm < 1e-10:
            return np.array([0, 0, 0])
        tangent = v / v_norm
        a_parallel = np.dot(a, tangent) * tangent
        a_perp = a - a_parallel
        perp_norm = np.linalg.norm(a_perp)
        if perp_norm < 1e-10:
            return np.array([0, 0, 0])
        return a_perp / perp_norm

    def binormal(self, t):
        """Tangent x Normal = Binormal. Perpendicular to both."""
        return np.cross(self.tangent(t), self.normal_vector(t))

    def torsion(self, t, dt=1e-6):
        """How much does the curve twist out of its plane?"""
        B_plus = np.cross(self.tangent(t + dt), self.normal_vector(t + dt))
        B_minus = np.cross(self.tangent(t - dt), self.normal_vector(t - dt))
        dB = (B_plus - B_minus) / (2 * dt)
        return -np.dot(dB, self.normal_vector(t))


# ================================================================
# PART 2: SURFACES - 2D sheets living in 3D space
# ================================================================

class Surface:
    """
    A parametric surface in 3D space.

    Imagine a rubber sheet. You can label each point with two numbers
    (u, v) like latitude and longitude.
    """

    def __init__(self, x_func, y_func, z_func, u_range=(-1, 1), v_range=(-1, 1)):
        self.x = x_func
        self.y = y_func
        self.z = z_func
        self.u_min, self.u_max = u_range
        self.v_min, self.v_max = v_range

    def position(self, u, v):
        return np.array([self.x(u, v), self.y(u, v), self.z(u, v)])

    def partial_u(self, u, v, du=1e-6):
        """Tangent vector in the u-direction."""
        return (self.position(u + du, v) - self.position(u - du, v)) / (2 * du)

    def partial_v(self, u, v, dv=1e-6):
        """Tangent vector in the v-direction."""
        return (self.position(u, v + dv) - self.position(u, v - dv)) / (2 * dv)

    def normal(self, u, v):
        """Unit normal vector - perpendicular to the surface."""
        n = np.cross(self.partial_u(u, v), self.partial_v(u, v))
        n_norm = np.linalg.norm(n)
        if n_norm < 1e-10:
            return np.array([0, 0, 0])
        return n / n_norm

    def first_fundamental_form(self, u, v):
        """
        Measures distances on the surface (intrinsic geometry).
        I = [[E, F], [F, G]]
        E = r_u.r_u, F = r_u.r_v, G = r_v.r_v
        """
        r_u = self.partial_u(u, v)
        r_v = self.partial_v(u, v)
        E = np.dot(r_u, r_u)
        F = np.dot(r_u, r_v)
        G = np.dot(r_v, r_v)
        return np.array([[E, F], [F, G]])

    def surface_area_element(self, u, v):
        """dA = sqrt(EG - F^2) du dv"""
        return np.sqrt(np.linalg.det(self.first_fundamental_form(u, v)))

    def second_fundamental_form(self, u, v):
        """
        Measures how the surface curves (extrinsic geometry).
        II = [[L, M], [M, N]]
        """
        n = self.normal(u, v)
        du, dv = 1e-5, 1e-5
        r_uu = (self.partial_u(u + du, v) - self.partial_u(u - du, v)) / (2 * du)
        r_vv = (self.partial_v(u, v + dv) - self.partial_v(u, v - dv)) / (2 * dv)
        r_uv = (self.partial_u(u, v + dv) - self.partial_u(u, v - dv)) / (2 * dv)
        L = np.dot(r_uu, n)
        M = np.dot(r_uv, n)
        N = np.dot(r_vv, n)
        return np.array([[L, M], [M, N]])

    def shape_operator(self, u, v):
        """S = I^-1 * II. Eigenvalues are principal curvatures."""
        I = self.first_fundamental_form(u, v)
        II = self.second_fundamental_form(u, v)
        try:
            return np.linalg.inv(I) @ II
        except np.linalg.LinAlgError:
            return np.zeros((2, 2))

    def principal_curvatures(self, u, v):
        """k1, k2 — max and min curvatures at this point."""
        eigenvalues = np.linalg.eigvals(self.shape_operator(u, v))
        return sorted(eigenvalues, key=abs, reverse=True)

    def gaussian_curvature(self, u, v):
        """
        K = k1 * k2
        K > 0: sphere-like, K < 0: saddle-like, K = 0: flat/cylindrical
        Intrinsic — an ant on the surface can measure this.
        """
        k1, k2 = self.principal_curvatures(u, v)
        return k1 * k2

    def mean_curvature(self, u, v):
        """H = (k1 + k2) / 2. H = 0 means minimal surface (soap film)."""
        k1, k2 = self.principal_curvatures(u, v)
        return (k1 + k2) / 2


# ================================================================
# PART 3: GEODESICS - "Straight Lines" on Curved Surfaces
# ================================================================

class Geodesic:
    """
    Geodesic paths on a surface.

    If you're an ant walking on the surface going "straight ahead"
    (not turning left or right), you follow a geodesic.
    """

    def __init__(self, surface):
        self.surf = surface

    def christoffel_symbols(self, u, v):
        """
        Gamma^a_bc — how coordinate lines bend on the surface.
        Formula: Gamma^a_bc = 1/2 * g^ad (dg_db/dx^c + dg_dc/dx^b - dg_bc/dx^d)
        """
        du, dv = 1e-5, 1e-5
        g = self.surf.first_fundamental_form(u, v)
        g_u_plus = self.surf.first_fundamental_form(u + du, v)
        g_u_minus = self.surf.first_fundamental_form(u - du, v)
        g_v_plus = self.surf.first_fundamental_form(u, v + dv)
        g_v_minus = self.surf.first_fundamental_form(u, v - dv)
        dg_du = (g_u_plus - g_u_minus) / (2 * du)
        dg_dv = (g_v_plus - g_v_minus) / (2 * dv)

        E, F, G = g[0, 0], g[0, 1], g[1, 1]
        E_u, F_u, G_u = dg_du[0, 0], dg_du[0, 1], dg_du[1, 1]
        E_v, F_v, G_v = dg_dv[0, 0], dg_dv[0, 1], dg_dv[1, 1]

        det_g = E * G - F * F
        if abs(det_g) < 1e-10:
            return np.zeros((2, 2, 2))
        g_inv = np.array([[G, -F], [-F, E]]) / det_g

        Gamma = np.zeros((2, 2, 2))
        Gamma[0, 0, 0] = 0.5 * g_inv[0, 0] * E_u + 0.5 * g_inv[0, 1] * (2 * F_u - E_v)
        Gamma[0, 0, 1] = 0.5 * g_inv[0, 0] * E_v + 0.5 * g_inv[0, 1] * G_u
        Gamma[0, 1, 0] = Gamma[0, 0, 1]
        Gamma[0, 1, 1] = 0.5 * g_inv[0, 0] * (2 * F_v - G_u) + 0.5 * g_inv[0, 1] * G_v
        Gamma[1, 0, 0] = 0.5 * g_inv[1, 0] * E_u + 0.5 * g_inv[1, 1] * (2 * F_u - E_v)
        Gamma[1, 0, 1] = 0.5 * g_inv[1, 0] * E_v + 0.5 * g_inv[1, 1] * G_u
        Gamma[1, 1, 0] = Gamma[1, 0, 1]
        Gamma[1, 1, 1] = 0.5 * g_inv[1, 0] * (2 * F_v - G_u) + 0.5 * g_inv[1, 1] * G_v
        return Gamma

    def geodesic_equation(self, state):
        """
        d^2u^a/dt^2 + Gamma^a_bc (du^b/dt)(du^c/dt) = 0
        Returns [du/dt, dv/dt, d^2u/dt^2, d^2v/dt^2]
        """
        u, v, u_dot, v_dot = state
        Gamma = self.christoffel_symbols(u, v)
        u_ddot = -(Gamma[0, 0, 0] * u_dot * u_dot +
                   2 * Gamma[0, 0, 1] * u_dot * v_dot +
                   Gamma[0, 1, 1] * v_dot * v_dot)
        v_ddot = -(Gamma[1, 0, 0] * u_dot * u_dot +
                   2 * Gamma[1, 0, 1] * u_dot * v_dot +
                   Gamma[1, 1, 1] * v_dot * v_dot)
        return np.array([u_dot, v_dot, u_ddot, v_ddot])

    def compute(self, u0, v0, direction, length=10, n_points=1000):
        """Compute a geodesic from (u0,v0) in given direction using RK4."""
        direction = np.array(direction, dtype=float)
        direction = direction / np.linalg.norm(direction)
        dt = length / n_points
        state = np.array([u0, v0, direction[0], direction[1]])
        path_3d = np.zeros((n_points, 3))
        path_3d[0] = self.surf.position(u0, v0)
        for i in range(1, n_points):
            k1 = self.geodesic_equation(state)
            k2 = self.geodesic_equation(state + 0.5 * dt * k1)
            k3 = self.geodesic_equation(state + 0.5 * dt * k2)
            k4 = self.geodesic_equation(state + dt * k3)
            state = state + (dt / 6) * (k1 + 2*k2 + 2*k3 + k4)
            path_3d[i] = self.surf.position(state[0], state[1])
        return path_3d


# ================================================================
# VERIFICATION TESTS
# ================================================================

def run_tests():
    print("\n" + "=" * 60)
    print("PRACTICAL VERIFICATIONS")
    print("=" * 60)

    # Test 1: Circle curvature = 1/R
    circle_r2 = Curve(lambda t: 2*np.cos(t), lambda t: 2*np.sin(t), lambda t: 0)
    k = circle_r2.curvature(0)
    print(f"\n1. CIRCLE (R=2): curvature = {k:.4f} (expected 0.5) {'PASS' if abs(k - 0.5) < 0.01 else 'FAIL'}")

    # Test 2: Straight line curvature = 0
    line = Curve(lambda t: t, lambda t: 2*t, lambda t: 3*t)
    k = line.curvature(1.0)
    print(f"2. STRAIGHT LINE: curvature = {k:.6f} (expected 0) {'PASS' if k < 0.001 else 'FAIL'}")

    # Test 3: Sphere K = 1/R^2
    sphere = Surface(
        lambda u, v: np.cos(u)*np.sin(v),
        lambda u, v: np.sin(u)*np.sin(v),
        lambda u, v: np.cos(v),
        u_range=(0, 2*np.pi), v_range=(0.1, np.pi-0.1)
    )
    K = sphere.gaussian_curvature(np.pi/4, np.pi/3)
    print(f"3. UNIT SPHERE: K = {K:.4f} (expected 1.0) {'PASS' if abs(K - 1.0) < 0.01 else 'FAIL'}")

    # Test 4: Plane K = 0
    plane = Surface(lambda u, v: u, lambda u, v: v, lambda u, v: 0)
    K = plane.gaussian_curvature(0.5, 0.5)
    print(f"4. PLANE: K = {K:.6f} (expected 0) {'PASS' if abs(K) < 0.001 else 'FAIL'}")

    # Test 5: Cylinder K = 0
    cylinder = Surface(
        lambda u, v: np.cos(u), lambda u, v: np.sin(u), lambda u, v: v
    )
    K = cylinder.gaussian_curvature(np.pi/4, 1)
    print(f"5. CYLINDER: K = {K:.6f} (expected 0) {'PASS' if abs(K) < 0.001 else 'FAIL'}")

    print("\nALL TESTS COMPLETE")


if __name__ == "__main__":
    run_tests()
