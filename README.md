# MSREⅡ — 熔盐堆系统瞬态仿真器

本项目为研究与控制熔盐堆系统的高性能瞬态模拟框架，支持点堆中子动力学、热构件换热、水力学分析、多变量控制（PID/MPC）、数据记录与可视化。

## 🔧 模块结构

- `main.py`：主仿真循环
- `input_card.yaml`：仿真参数配置
- `core/`：核心物理模块（neutronics, thermal, hydraulics）
- `controllers/`：控制模块（PID, SCRAM, MPC）
- `utils/`：数据记录、日志与可视化工具
- `outputs/`：仿真结果数据

鸿强，很棒，我们已经搭建起一个高度模块化、面向熔盐堆瞬态仿真的完整模拟项目⚛️🛠️。我来帮你梳理一下 **整体结构布局** 与 **仿真运行流程**，让你后续查阅、维护、拓展都如顺手拧螺丝🔧。

---

## 🗂 项目结构总览：MSREⅡ 仿真框架

```text
E:\code\MSREⅡ\
│
├── main.py                  # 🔁 主仿真主循环入口（协调所有模块）
├── input_card.yaml          # 📥 输入卡：定义几何参数、控制器配置等
├── requirements.txt         # 📦 所需依赖库列表（numpy, pandas, matplotlib等）
│
├── core/                    # 💠 核心物理模块
│   ├── input_parser.py      # 读取 & 解析 input_card.yaml 配置
│   ├── hydraulics.py        # 流体 & 水力学参数求解器
│   ├── neutronics.py        # 点堆中子动力学模型（含缓发前体延迟）
│   ├── io_interface.py      # 与外部系统交互的 I/O 接口（JSON/CSV/Socket）
│   └── thermal_structure/
│       ├── one_d.py         # 1D 热传导模块（TDMA隐式求解）
│       └── two_d.py         # 2D 热传导模块（径向-轴向 ADI）
│
├── controllers/             # 🎛️ 控制模块（反应堆功率 & 热工耦合控制）
│   ├── control.py           # 增量式 PID 控制器
│   ├── logic.py             # 布尔开关逻辑控制器（SCRAM触发等）
│   ├── mpc.py               # MPC 占位控制器（未来支持优化策略）
│   └── manager.py           # 控制中心 ControlManager（调度 & 故障切换）
│
├── solver/
│   └── tdma.py              # TDMA 三对角求解器，用于热传导离散解
│
├── utils/                   # 🧰 工具模块
│   ├── data_recorder.py     # 数据记录器（保存标量 & 数组变量）
│   ├── logger.py            # 日志记录器（保存控制轨迹与事件）
│   └── visualization/
│       ├── output.py        # 保存结果为 CSV/NPY 等格式
│       └── plotting.py      # 绘图函数（温度曲线、功率分布等）
│
└── outputs/                 # 📤 仿真输出结果（数据、日志、图片）
    └── run1/
        ├── scalars.csv      # 时间序列数据记录
        ├── T_core.npy       # 温度分布随时间演化
        ├── control_trace.csv
        └── event_log.txt
```

---

## 🔁 仿真运行顺序：主流程逻辑图

参考你文献中的图 25，我们在 `main.py` 中实现的运行顺序是：

1. **读取输入卡 → 参数初始化**
   - 调用 `input_parser.py` 加载 `input_card.yaml`
   - 初始化几何结构、网格、初始温度、功率分布

2. **模块初始化**
   - 中子模块 `neutronics.py`
   - 热构件模块 `thermal_structure/one_d.py` 或 `two_d.py`
   - 水力学模块 `hydraulics.py`
   - 控制器 `ControlManager`（包含 PID, MPC, SCRAM）
   - 记录模块 `DataRecorder` 与 `SimulationLogger`
   - 外部接口 `IOInterface`（支持参数传入与结果导出）

3. **进入时间推进循环**
   - 每步：更新控制器 → 得到 `ρ`, `U`, `SCRAM`
   - 推进中子动力学模块 → 更新 `n(t)`、功率源项
   - 推进热模块 → 更新温度分布
   - 推进水力学模块 → 更新密度、速度、压强、焓
   - 写入数据记录模块 → 保存标量与数组
   - 日志记录控制行为与状态变化
   - 可选地将状态发送至外部（CSV/Socket）

4. **仿真结束后统一导出**
   - CSV/Numpy 格式输出（便于分析/绘图/后处理）
   - 控制器行为日志 & 事件日志保存
   - 可视化模块生成图像或动画

---

## ✅ 项目部署与运行方法

```bash
cd E:\code\MSREⅡ
pip install -r requirements.txt
python main.py
```

你可以根据需要修改 `input_card.yaml` 来设定不同的反应性、控制目标、初始温度、边界条件等。控制模块支持自动故障检测与模式切换，热模块可拓展为 TRISO 燃料、2D耦合等。


