鸿强，来啦 ✅！我们现在为你的系统打造一个更高级的 **SimulationLogger**，它比 `DataRecorder` 更有“大脑味”：它不仅记录数据，还记录事件、控制行为、模块状态变化，并具备结构化导出、分级日志、可筛选机制，最终可以服务于：

- 🧪 数据分析（温度曲线、控制器响应、功率变化）  
- 📊 仿真仪表板可视化（Streamlit / Dashboard）  
- 🧠 模型调试与异常诊断（哪些模块何时发生了什么）

---

## 📁 推荐模块路径：`utils/logger.py`

你主控逻辑中只需：

```python
from utils.logger import SimulationLogger
logger = SimulationLogger("outputs/run1")
```

---

## 🧱 类结构设计草图

```python
import os
import csv
import datetime

class SimulationLogger:
    """
    高级仿真日志器：记录数据、事件、控制行为、状态变化
    """

    def __init__(self, output_dir="outputs"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

        # 准备文件路径
        self.data_file = os.path.join(self.output_dir, "data_log.csv")
        self.event_file = os.path.join(self.output_dir, "event_log.txt")
        self.control_file = os.path.join(self.output_dir, "control_trace.csv")

        # 写入头
        with open(self.data_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Step", "Time(s)", "T_out(K)", "n", "rho", "U", "SCRAM"])
        with open(self.control_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Step", "Mode", "T_out", "Error_T", "U", "Error_n", "rho", "SCRAM"])
        with open(self.event_file, 'w') as f:
            f.write(f"=== Simulation Log Started at {datetime.datetime.now()} ===\n")

    def log_data(self, step, time_s, T_out, n, rho, U, scram):
        with open(self.data_file, 'a', newline='') as f:
            csv.writer(f).writerow([step, time_s, T_out, n, rho, U, int(scram)])

    def log_control(self, step, mode, error_T, U, error_n, rho, scram):
        with open(self.control_file, 'a', newline='') as f:
            csv.writer(f).writerow([step, mode, f"{T_out:.2f}", f"{error_T:.3f}", f"{U:.1f}", f"{error_n:.3f}", f"{rho:.5f}", int(scram)])

    def log_event(self, message):
        with open(self.event_file, 'a') as f:
            f.write(f"[{datetime.datetime.now()}] {message}\n")

    def finalize(self):
        with open(self.event_file, 'a') as f:
            f.write(f"=== Simulation Ended at {datetime.datetime.now()} ===\n")
```

---

## 🧩 使用方式示例

```python
from utils.logger import SimulationLogger
logger = SimulationLogger("outputs/run_T_step")

# 每步写入数据与控制行为
logger.log_data(step, t, T_out, n, rho, U, scram)
logger.log_control(step, ctrl.control_mode, error_T, U, error_n, rho, scram)

# 写入事件日志
if scram:
    logger.log_event("SCRAM activated due to over-temperature")

# 结束
logger.finalize()
```

---

## 🔍 整体结构输出如下：

```
outputs/
└── run_T_step/
    ├── data_log.csv          ← 核心物理变量时序表
    ├── control_trace.csv     ← 控制器输出与误差追踪
    └── event_log.txt         ← 可读事件日志（异常、状态变化）
```

---

## 🔮 未来升级方向

| 模块              | 功能                                       |
|-------------------|---------------------------------------------|
| `SimulationAnalyzer` | 从 `data_log.csv` 中提取 KPIs、响应时间、超调等 |
| `SimulationPlotter`  | 自动绘制控制曲线、功率变化图、温度热图           |
| 日志等级系统         | 支持 info / warn / error 分级输出              |
| 异常分类              | 多类事件标记（SCRAM、流量异常、PID震荡等）        |
| Streamlit GUI       | 即时显示 log → 仿真可视仪表板 🧭              |

---

如果你希望，我可以直接将 `SimulationLogger` 添加进你的模拟主循环中，并调用 `logger.log_XXX()` 方法记录关键变量和状态变化。或者我也可以结合 `DataRecorder` 抽象出一个复合结构，用于“轻量日志 + 高频数据”双通道记录系统📋📊

你想接下来导出个完整测试报告？还是来个“热暴冲突发事件”模拟检验控制响应？⏱️🔥📉