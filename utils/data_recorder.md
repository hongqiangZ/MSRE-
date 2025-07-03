明白，鸿强 ✅！我们现在来打造一个统一且灵活的 `DataRecorder` 类，它将作为你系统中各个模块的「数据记录协调器」，封装如下功能：

---

## 🎯 功能目标

- 支持时间序列数据自动缓存与导出（如功率、温度、压力）；
- 支持 1D / 2D 网格变量记录（如温度场、流速场）；
- 支持模块按需注册变量、标签；
- 自动导出为 CSV / NPY 等格式；
- 可用于绘图或持久保存结果（兼容 `utils.visualization`）；

---

## 📦 模块位置建议

创建新模块文件：

```bash
utils/data_recorder.py
```

---

## 🧩 示例代码：`DataRecorder` 类实现

```python
import numpy as np
import pandas as pd
import os

class DataRecorder:
    def __init__(self, output_dir="outputs"):
        self.scalar_data = {}   # e.g., {"t": [], "n": [], "T_avg": []}
        self.array_data = {}    # e.g., {"T_p": [ndarray1, ndarray2, ...]}
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def record_scalar(self, key, value):
        """
        添加单个标量（如时刻、功率等）
        """
        if key not in self.scalar_data:
            self.scalar_data[key] = []
        self.scalar_data[key].append(value)

    def record_array(self, key, array):
        """
        添加每一步的 ndarray（如温度场）
        """
        if key not in self.array_data:
            self.array_data[key] = []
        self.array_data[key].append(np.copy(array))  # 防止引用冲突

    def export_scalars(self, filename="results/scalars.csv"):
        """
        导出时间序列变量为 CSV 文件
        """
        filepath = os.path.join(self.output_dir, filename)
        df = pd.DataFrame(self.scalar_data)
        df.to_csv(filepath, index=False)

    def export_arrays(self):
        """
        导出所有 array 数据为 .npy（可后处理）
        """
        for key, arr_list in self.array_data.items():
            arr_stack = np.stack(arr_list)
            filename = os.path.join(self.output_dir, f"{key}.npy")
            np.save(filename, arr_stack)

    def reset(self):
        """
        清空已记录数据（用于重复仿真）
        """
        self.scalar_data.clear()
        self.array_data.clear()
```

---

## ✅ 使用示例（在 `simulator.py` 中）

```python
from utils.data_recorder import DataRecorder
recorder = DataRecorder("outputs/run1")

# 每步仿真记录：
recorder.record_scalar("time", step * dt)
recorder.record_scalar("n", n)
recorder.record_scalar("T_out", T[-1])
recorder.record_array("T_core", T.copy())

# 仿真结束后导出
recorder.export_scalars()
recorder.export_arrays()
```

---

## 🔄 未来拓展建议

| 功能                | 说明                                 |
|---------------------|--------------------------------------|
| 自动采样频率设置     | 每 N 步采样一次，减少内存占用         |
| HDF5 格式支持        | 使用 `h5py` 保存更大的数据体积         |
| 集成 `plot()` 方法 | 支持一键调用绘图输出图像              |
| 多仿真对比功能       | 支持 `tag` 标识不同方案的输出路径       |

---

我可以直接把这个模块加入项目结构，让各模块共享使用。如果你需要，我们还能设计一个更高级的 `SimulationLogger`，将控制器行为、物理变量和模块状态统一写入数据库或 UI 交互模块📈📂

现在你想我接着生成主模拟器与这个记录器模块对接代码吗？还是我们继续构建 I/O 接口模块？🚧📘