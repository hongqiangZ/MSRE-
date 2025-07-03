import numpy as np

def upstream(var_left, var_right, u):
    """一阶迎风格式：根据速度方向选择上游变量"""
    return var_left if u >= 0 else var_right


def update_hydraulics(
    rho, u, p, H, dx, dt,
    sin_theta=0.0, g=9.81,
    A=0.01, Av=0.01,
    friction=0.0,
    pump_head=0.0
):
    """
    熔盐堆流体系统的一维瞬态流体动力学更新（半隐式格式）
    """

    N = len(rho)
    rho_new = rho.copy()
    u_new = u.copy()
    p_new = p.copy()
    H_new = H.copy()

    for i in range(1, N-1):
        # 主控制体参数
        rho_i, rho_im1 = rho[i], rho[i - 1]
        H_i, H_im1 = H[i], H[i - 1]

        # 动量控制体速度（位于 i 节点）
        u_i, u_im1 = u[i], u[i - 1]

        # 状态方程导数（可设常数）
        drho_dH = -0.0001  # N(H, P) 中对 H 的偏导数
        drho_dp = 0.00001  # N(H, P) 中对 P 的偏导数

        # --- 1. 质量守恒 ---
        mass_flux_in = upstream(rho_im1, rho_i, u_im1) * u_im1 * Av
        mass_flux_out = upstream(rho_i, rho[i+1], u_i) * u_i * Av
        drho_dt = -(mass_flux_out - mass_flux_in) / dx
        rho_new[i] += drho_dt * dt

        # --- 2. 动量守恒 ---
        du_dt = (
            - (rho[i]*u[i]**2 + p[i] - rho[i-1]*u[i-1]**2 - p[i-1]) / dx
            - rho[i] * g * sin_theta
            - friction * u[i]
        ) / rho[i]
        u_new[i] += du_dt * dt

        # --- 3. 能量守恒（简化忽略剪切/压降）---
        H_flux_in = rho_im1 * H_im1 * u_im1 * Av
        H_flux_out = rho_i * H_i * u_i * Av
        dH_dt = -(H_flux_out - H_flux_in) / (rho_i * A * dx)
        H_new[i] += dH_dt * dt

        # --- 4. 状态方程（ρ = ρ(p, H)）---
        rho_eos = rho_i + drho_dH * (H_new[i] - H_i) + drho_dp * (p[i] - p[i])
        # 可加入迭代解压强使得密度匹配

    return rho_new, u_new, p_new, H_new


