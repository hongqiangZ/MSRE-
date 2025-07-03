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
