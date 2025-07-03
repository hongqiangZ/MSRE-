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
