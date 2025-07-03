import numpy as np
from solver.tdma import tdma_solver

def solve_thermal_structure_2d(
    T, k, rho, cp, q, dr, dz, dt,
    geometry='cylinder',
    bc_r=('Symmetry', 'Robin'),
    bc_z=('Dirichlet', 'Dirichlet'),
    bc_val_r=(None, (100, 600)),
    bc_val_z=(800, 800)
):
    nz, nr = T.shape
    T_new = T.copy()

    # 径向方向
    for i in range(nz):
        a = np.zeros(nr - 1)
        b = np.zeros(nr)
        c = np.zeros(nr - 1)
        d = np.zeros(nr)

        for j in range(1, nr - 1):
            r = j * dr
            A_e, A_w = r + 0.5 * dr, r - 0.5 * dr
            ke = 2 * k[i, j] * k[i, j + 1] / (k[i, j] + k[i, j + 1])
            kw = 2 * k[i, j] * k[i, j - 1] / (k[i, j] + k[i, j - 1])
            ae = ke * A_e / dr
            aw = kw * A_w / dr
            ap = aw + ae + rho[i, j] * cp[i, j] * dr / dt
            a[j - 1], b[j], c[j - 1] = -aw, ap, -ae
            d[j] = rho[i, j] * cp[i, j] * T[i, j] * dr / dt + q[i, j] * dr

        if bc_r[0] == 'Symmetry':
            b[0], c[0], d[0] = 1.0, -1.0, 0.0
        elif bc_r[0] == 'Dirichlet':
            b[0], d[0] = 1.0, bc_val_r[0]
        elif bc_r[0] == 'Neumann':
            b[0], c[0] = 1.0, -1.0
            d[0] = dr * bc_val_r[0] / k[i, 0]

        if bc_r[1] == 'Robin':
            h, Tf = bc_val_r[1]
            a[-1] = -k[i, -1] / dr
            b[-1] = k[i, -1] / dr + h
            d[-1] = h * Tf
        elif bc_r[1] == 'Dirichlet':
            b[-1], d[-1] = 1.0, bc_val_r[1]
        elif bc_r[1] == 'Neumann':
            a[-1], b[-1] = -1.0, 1.0
            d[-1] = dr * bc_val_r[1] / k[i, -1]

        T_new[i, :] = tdma_solver(a, b, c, d)

    # 轴向方向
    for j in range(nr):
        a = np.zeros(nz - 1)
        b = np.zeros(nz)
        c = np.zeros(nz - 1)
        d = np.zeros(nz)

        for i in range(1, nz - 1):
            ke = 2 * k[i, j] * k[i + 1, j] / (k[i, j] + k[i + 1, j])
            kw = 2 * k[i, j] * k[i - 1, j] / (k[i, j] + k[i - 1, j])
            ae = ke / dz
            aw = kw / dz
            ap = aw + ae + rho[i, j] * cp[i, j] * dz / dt
            a[i - 1], b[i], c[i - 1] = -aw, ap, -ae
            d[i] = rho[i, j] * cp[i, j] * T_new[i, j] * dz / dt + q[i, j] * dz

        if bc_z[0] == 'Dirichlet':
            b[0], d[0] = 1.0, bc_val_z[0]
        elif bc_z[0] == 'Neumann':
            b[0], c[0] = 1.0, -1.0
            d[0] = dz * bc_val_z[0] / k[0, j]

        if bc_z[1] == 'Dirichlet':
            b[-1], d[-1] = 1.0, bc_val_z[1]
        elif bc_z[1] == 'Neumann':
            a[-1], b[-1] = -1.0, 1.0
            d[-1] = dz * bc_val_z[1] / k[-1, j]

        T_new[:, j] = tdma_solver(a, b, c, d)

    return T_new
