鸿强，我明白了✅！下面我会根据你模块体系的完整性，结合你PDF中描述的“程序运行流程”（图25），为你构建一个完整、模块化、可拓展的**模拟主循环主程序 `main.py`**：

它将实现：

- 📥 从输入卡中初始化所有模块所需参数；
- 🔗 调用参数初始化函数 `load_input_card`；
- ⚙️ 初始化中子、热、流体、水力、控制等模块；
- 🔁 进入时间推进循环，逐步推进系统状态；
- 🎛️ 动态调用控制模块调节反应性和热力边界；
- 💾 调用数据记录模块写出中间数据；
- 🖼️ 最后统一输出数据和可视化。

---

## 📁 `main.py` 主循环代码架构

```python
# main.py
from core.input_parser import load_input_card
from core.neutronics import PointKineticsWithDecay
from core.thermal_structure.one_d import solve_thermal_structure_1d
from core.hydraulics import update_hydraulics
from controllers.manager import ControlManager
from utils.data_recorder import DataRecorder
from utils.logger import SimulationLogger

import numpy as np
import os

def main():
    # === 1. 读取配置文件 ===
    params = load_input_card("input_card.yaml")
    neutronics_cfg    = params['neutronics']
    thermal1d_cfg     = params['thermal_1d']
    hydraulics_cfg    = params['hydraulics']
    control_cfg       = params['control']
    recorder_cfg      = params['recorder']

    dt = hydraulics_cfg['dt']
    steps = int(params['meta']['t_end'] / dt)

    # === 2. 初始化各模块 ===
    pk = PointKineticsWithDecay(**neutronics_cfg, dt=dt)

    N = hydraulics_cfg['N']
    dx = hydraulics_cfg['dr']
    x = np.linspace(0, N*dx, N)
    T = np.ones(N) * thermal1d_cfg.get('init_temp', 900)
    rho_f = np.ones(N) * hydraulics_cfg.get('rho_salt', 1800)
    cp_f  = np.ones(N) * hydraulics_cfg.get('cp', 1500)
    k_f   = np.ones(N) * thermal1d_cfg.get('k', 10)
    q     = np.zeros(N)

    u = np.ones(N) * hydraulics_cfg.get('u0', 1.0)
    p = np.ones(N) * hydraulics_cfg.get('p0', 1e5)
    H = np.ones(N) * hydraulics_cfg.get('H0', 2e5)

    ctrl = ControlManager(dt=dt)
    recorder = DataRecorder(recorder_cfg['output_dir'])
    logger = SimulationLogger(recorder_cfg['output_dir'])

    # === 3. 开始时间推进循环 ===
    for step in range(steps):
        t = step * dt

        # 控制器输入
        sensors = {
            'T_out': T[-1],
            'T_ref': params['control'].get('T_ref', 950),
            'n': pk.n,
            'n_ref': params['control'].get('n_ref', 1.0)
        }
        actions = ctrl.update(sensors, step)
        U = actions['U']
        rho = actions['rho']
        scram = actions['scram']
        if scram:
            rho = -0.01

        # === 中子动力学 ===
        n, C = pk.step(rho)

        # === 功率密度计算 ===
        P0 = n  # 假设归一化
        q[:] = P0 * params['meta'].get('Fp', 1.0)  # 简化功率分布

        # === 热工结构计算 ===
        T = solve_thermal_structure_1d(
            T=T, k=k_f, rho=rho_f, cp=cp_f, q=q,
            dx=dx, dt=dt,
            geometry=thermal1d_cfg['geometry'],
            bc_type=thermal1d_cfg['bc_type'],
            bc_value=thermal1d_cfg['bc_value']
        )

        # === 流体动力学计算 ===
        rho_f, u, p, H = update_hydraulics(rho_f, u, p, H, dx=dx, dt=dt, **hydraulics_cfg)

        # === 数据记录 ===
        recorder.record_scalar("time", t)
        recorder.record_scalar("n", n)
        recorder.record_scalar("T_out", T[-1])
        recorder.record_scalar("rho", rho)
        recorder.record_scalar("U", U)
        recorder.record_scalar("scram", scram)
        recorder.record_array("T_core", T)

        logger.log_data(step, t, T[-1], n, rho, U, scram)

    # === 4. 输出结果 ===
    recorder.export_scalars()
    recorder.export_arrays()
    logger.finalize()

    print("✅ 模拟完成。输出数据保存在:", recorder_cfg['output_dir'])

if __name__ == "__main__":
    main()
```

---

## 🧠 说明与设计亮点

| 设计点                     | 描述                                              |
|----------------------------|---------------------------------------------------|
| 面向配置卡驱动             | 所有关键数据均来自 `input_card.yaml`              |
| 模块解耦                   | 各功能逻辑清晰独立，可替换/关闭/调试               |
| SCRAM控制                  | 由 `ControlManager` 与逻辑模块判定，控制 ρ          |
| 数据记录分层               | `DataRecorder` 保存物理数据，`SimulationLogger` 保存控制行为 |
| 输出统一封装               | 所有导出数据集中于 outputs 子目录下，可后期可视化 |

---

我可以为你生成该文件写入 `E:\code\MSREⅡ\main.py`，也可以接着帮你创建：

- 📂 `input_card.yaml` 参数输入卡模板；
- 📂 `outputs/` 模拟输出数据；
- 🖼️ 可视化脚本和图像文件。

你是否现在希望我配套写一份简洁清晰的 `input_card.yaml`？或者我们进一步进入 GUI 接口或仿真参数扫描模式？🎛️✨你说了算！