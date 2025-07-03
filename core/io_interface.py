"""
IOInterface 模块 — 与外部系统进行数据交换的接口
支持文件读取、写入、Socket 通信等拓展方式
"""

import json
import pandas as pd
import socket

class IOInterface:
    """
    与外部系统进行数据交换的接口模块
    支持 JSON、CSV、Socket 等通信格式
    """

    def __init__(self, input_path=None, output_path=None):
        self.input_path = input_path
        self.output_path = output_path

    def read_input_json(self):
        """从 JSON 文件读取控制输入或设定参数"""
        if not self.input_path:
            return {}
        try:
            with open(self.input_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data
        except Exception as e:
            print(f"[IOInterface] 读取失败: {e}")
            return {}

    def write_output_csv(self, data_dict, filename="external_output.csv"):
        """将仿真结果写入 CSV 文件"""
        try:
            df = pd.DataFrame(data_dict)
            df.to_csv(filename, index=False)
            print(f"[IOInterface] 已写入输出结果: {filename}")
        except Exception as e:
            print(f"[IOInterface] 写入失败: {e}")

    def send_to_socket(self, ip="127.0.0.1", port=9999, payload="status OK"):
        """向远程 Socket 发送仿真状态（可用于嵌入式或实时系统）"""
        try:
            s = socket.socket()
            s.connect((ip, port))
            s.send(payload.encode('utf-8'))
            s.close()
        except Exception as e:
            print(f"[IOInterface] Socket发送失败: {e}")
