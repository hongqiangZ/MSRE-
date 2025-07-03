import numpy as np
from solver.tdma import tdma_solver

def solve_thermal_structure_1d(
    T, k, rho, cp, q, dx, dt, geometry='cartesian',
    bc_type=('Dirichlet', 'Robin'),
    bc_value=(300, (30, 300))
):
    N = len(T)
    a = np.zeros(N - 1)
    b = np.zeros(N)
    c = np.zeros(N - 1)
    d = np.zeros(N)

    def A(x):  # 面积因子
        if geometry == 'cartesian': return 1.0
        elif geometry == 'cylinder': return x
        elif geometry == 'sphere': return x**2
        else: raise ValueError("Unsupported geometry")

    for i in range(1, N - 1):
        xm, xp = (i - 0.5) * dx, (i + 0.5) * dx
        A_w, A_e = A(xm), A(xp)

        kw = 2 * k[i] * k[i - 1] / (k[i] + k[i - 1])
        ke = 2 * k[i] * k[i + 1] / (k[i] + k[i + 1])

        aw = kw * A_w / dx
        ae = ke * A_e / dx
        ap = aw + ae + rho[i] * cp[i] * dx / dt

        a[i - 1] = -aw
        b[i] = ap
        c[i] = -ae
        d[i] = rho[i] * cp[i] * T[i] * dx / dt + q[i] * dx

    # 左边界
    if bc_type[0] == 'Dirichlet':
        b[0], c[0], d[0] = 1.0, 0.0, bc_value[0]
    elif bc_type[0] == 'Neumann':
        b[0], c[0] = 1.0, -1.0
        d[0] = dx * bc_value[0] / k[0]
    elif bc_type[0] == 'Robin':
        h, T_inf = bc_value[0]
        b[0] = k[0] / dx + h
        c[0] = -k[0] / dx
        d[0] = h * T_inf

    # 右边界
    if bc_type[1] == 'Dirichlet':
        a[-1], b[-1], d[-1] = 0.0, 1.0, bc_value[1]
    elif bc_type[1] == 'Neumann':
        a[-1], b[-1] = -1.0, 1.0
        d[-1] = dx * bc_value[1] / k[-1]
    elif bc_type[1] == 'Robin':
        h, T_inf = bc_value[1]
        a[-1] = -k[-1] / dx
        b[-1] = k[-1] / dx + h
        d[-1] = h * T_inf

    return tdma_solver(a, b, c, d)
