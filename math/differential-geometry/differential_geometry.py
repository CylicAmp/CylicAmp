"""
Parametric surfaces and geodesics via numerical differentiation.

Provides Surface (position, tangent vectors, normal, first/second
fundamental forms, Gaussian curvature) and Geodesic (Christoffel symbols),
used by tensors_riemann_parallel_transport.py.
"""

import numpy as np


class Surface:
    def __init__(self, x_func, y_func, z_func, u_range, v_range, h=1e-5):
        self.x_func = x_func
        self.y_func = y_func
        self.z_func = z_func
        self.u_range = u_range
        self.v_range = v_range
        self.h = h

    def position(self, u, v):
        return np.array([self.x_func(u, v), self.y_func(u, v), self.z_func(u, v)])

    def partial_u(self, u, v):
        h = self.h
        return (self.position(u + h, v) - self.position(u - h, v)) / (2 * h)

    def partial_v(self, u, v):
        h = self.h
        return (self.position(u, v + h) - self.position(u, v - h)) / (2 * h)

    def partial_uu(self, u, v):
        h = self.h
        return (self.position(u + h, v) - 2 * self.position(u, v) + self.position(u - h, v)) / (h * h)

    def partial_vv(self, u, v):
        h = self.h
        return (self.position(u, v + h) - 2 * self.position(u, v) + self.position(u, v - h)) / (h * h)

    def partial_uv(self, u, v):
        h = self.h
        return (self.position(u + h, v + h) - self.position(u + h, v - h)
                - self.position(u - h, v + h) + self.position(u - h, v - h)) / (4 * h * h)

    def normal(self, u, v):
        n = np.cross(self.partial_u(u, v), self.partial_v(u, v))
        norm = np.linalg.norm(n)
        return n / norm if norm > 1e-12 else n

    def first_fundamental_form(self, u, v):
        r_u = self.partial_u(u, v)
        r_v = self.partial_v(u, v)
        E = np.dot(r_u, r_u)
        F = np.dot(r_u, r_v)
        G = np.dot(r_v, r_v)
        return np.array([[E, F], [F, G]])

    def second_fundamental_form(self, u, v):
        n = self.normal(u, v)
        L = np.dot(self.partial_uu(u, v), n)
        M = np.dot(self.partial_uv(u, v), n)
        N = np.dot(self.partial_vv(u, v), n)
        return np.array([[L, M], [M, N]])

    def gaussian_curvature(self, u, v):
        g = self.first_fundamental_form(u, v)
        b = self.second_fundamental_form(u, v)
        det_g = g[0, 0] * g[1, 1] - g[0, 1] * g[1, 0]
        det_b = b[0, 0] * b[1, 1] - b[0, 1] * b[1, 0]
        if abs(det_g) < 1e-12:
            return 0.0
        return det_b / det_g


class Geodesic:
    def __init__(self, surface, h=1e-5):
        self.surf = surface
        self.h = h

    def christoffel_symbols(self, u, v):
        """
        Christoffel symbols of the second kind, Gamma[k, i, j], from the metric:
        Gamma^k_ij = 1/2 g^kl (d_i g_jl + d_j g_il - d_l g_ij)
        """
        h = self.h
        g = self.surf.first_fundamental_form(u, v)
        dg = [
            (self.surf.first_fundamental_form(u + h, v) - self.surf.first_fundamental_form(u - h, v)) / (2 * h),
            (self.surf.first_fundamental_form(u, v + h) - self.surf.first_fundamental_form(u, v - h)) / (2 * h),
        ]

        det_g = g[0, 0] * g[1, 1] - g[0, 1] * g[1, 0]
        if abs(det_g) < 1e-12:
            g_inv = np.zeros((2, 2))
        else:
            g_inv = np.array([[g[1, 1], -g[0, 1]], [-g[1, 0], g[0, 0]]]) / det_g

        Gamma = np.zeros((2, 2, 2))
        for k in range(2):
            for i in range(2):
                for j in range(2):
                    s = 0.0
                    for l in range(2):
                        s += g_inv[k, l] * (dg[i][j, l] + dg[j][i, l] - dg[l][i, j])
                    Gamma[k, i, j] = 0.5 * s
        return Gamma
