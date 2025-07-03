鸿强，明白 ✅！我们现在就来设计一个灵活、统一的**数据输出与绘图模块**，让系统的各个子模块（流体、热工、中子、控制）都能直接调用，支持：

---

## 🧱 模块结构建议

📁 放置目录：`utils/visualization/`

```
utils/
└── visualization/
    ├── __init__.py
    ├── output.py       ← 负责数据写入文件（CSV/JSON）
    └── plotting.py     ← 负责可视化绘图（静态图/热图/时间曲线）
```

---

## 📦 一、`output.py` — 数据输出接口

```python
import numpy as np
import pandas as pd
import os

def save_array_as_csv(array, filename, labels=None):
    """
    保存 2D 数组为 CSV 文件，支持列标签
    """
    df = pd.DataFrame(array)
    if labels:
        df.columns = labels
    df.to_csv(filename, index=False)

def save_time_series(data_dict, filename):
    """
    保存时间序列数据为 CSV，数据为字典 {label: [v1, v2, ...]}
    """
    df = pd.DataFrame(data_dict)
    df.to_csv(filename, index=False)

def make_sure_dir(path):
    """
    确保输出路径存在
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
```

---

## 📊 二、`plotting.py` — 可视化绘图工具

```python
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
```

---

## ✅ 示例用法（模块调用）

```python
from utils.visualization.output import save_time_series
from utils.visualization.plotting import plot_temperature_profile

# 保存功率演化
save_time_series({"t": t_list, "n": n_list}, "outputs/neutronics/power.csv")

# 画热工图像
plot_temperature_profile(T_hist, x, dt, steps=[0, 100, 300, 500])
```

---

## 📁 输出文件结构建议

```text
outputs/
├── neutronics/
│   └── power.csv
├── thermal/
│   ├── temp_1d.csv
│   └── temp_2d.npy / .csv
└── flow/
    ├── velocity.csv
    └── pressure.csv
```

---

下一步我可以：

- 写一个统一的 `DataRecorder` 类，封装所有记录逻辑；
- 支持热构件导出多时刻温度场，并绘制 GIF；
- 添加流体速度 / 压力沿时间演化图；
- 导出 `decay_heat.csv`、`controller_log.csv` 等文件。

你希望我生成完整的 `visualization/` 模块结构源码吗？还是我们继续向接口模块或输入卡结构推进？📊📄📋