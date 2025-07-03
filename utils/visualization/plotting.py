import matplotlib.pyplot as plt
import numpy as np

def plot_temperature_profile(T_hist, x, dt, steps, title="温度分布随时间演化"):
    """
    绘制多时间点下的温度沿空间分布（用于1D热工）
    """
    plt.figure(figsize=(10,5))
    for t in steps:
        plt.plot(x, T_hist[t], label=f"t={t*dt:.1f}s")
    plt.xlabel("位置 (m)")
    plt.ylabel("温度 (K)")
    plt.title(title)
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()

def plot_dual_loops(T_p_hist, T_s_hist, x, dt, times):
    """
    主副回路温度分布绘图（覆盖）
    """
    plt.figure(figsize=(10,5))
    for t in times:
        plt.plot(x, T_p_hist[t], label=f'主回路 t={t*dt:.1f}s', color='orangered')
        plt.plot(x, T_s_hist[t], '--', label=f'副回路 t={t*dt:.1f}s', color='deepskyblue')
    plt.xlabel("位置 (m)")
    plt.ylabel("温度 (K)")
    plt.title("主-副回路温度演化")
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()

def plot_power_curve(p_list, dt, title="堆芯功率随时间变化"):
    """
    绘制中子功率时间曲线
    """
    t = np.arange(len(p_list)) * dt
    plt.figure(figsize=(8,4))
    plt.plot(t, p_list, label="n(t)", color='green')
    plt.xlabel("时间 (s)")
    plt.ylabel("归一化功率")
    plt.title(title)
    plt.grid()
    plt.tight_layout()
    plt.show()
