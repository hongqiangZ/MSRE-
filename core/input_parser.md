下面是在 `core/input_parser.py` 中定义的通用输入卡解析器，它会根据文件后缀自动读取 YAML/JSON 格式的配置，并为所有核心模块（中子动力学、热构件、流体、水力学、控制、数据记录与可视化）提取对应参数字典：

```python
# core/input_parser.py

import os
import yaml
import json

def load_input_card(filepath: str) -> dict:
    """
    读取输入卡（YAML 或 JSON），返回完整配置字典，分模块提取子参数。

    输入配置示例 (YAML):
    --------------------------------------------------
    neutronics:
      beta_i: [2.11e-4, 1.395e-3, ..., 2.0e-5]
      lambda_i: [1.24e-2, 3.05e-2, ..., 2.26e-2]
      Lambda: 1e-4
      T_c: 2.0
      tau: 4.0

    thermal_1d:
      geometry: cylinder
      bc_type: [Dirichlet, Robin]
      bc_value: [300, [30, 300]]

    thermal_2d:
      geometry: cylinder
      bc_r: [Symmetry, Robin]
      bc_z: [Dirichlet, Dirichlet]
      bc_val_r: [null, [100, 600]]
      bc_val_z: [800, 800]

    hydraulics:
      dr: 0.01
      dz: 0.01
      dt: 0.01
      g: 9.81
      friction: 0.01
      A: 0.01
      Av: 0.01
      pump_head: 0.0

    control:
      pid_temp:
        Kp: 2000
        Ti: 50
        Td: 300
        limits: [1000, 20000]
      pid_rho:
        Kp: 500
        Ti: 100
        Td: 10
        limits: [-0.01, 0.01]
      mpc:
        horizon: 10

    recorder:
      output_dir: outputs/run1
      scalar_keys: [time, n, T_out]
      array_keys: [T_core]

    visualization:
      plot_steps: [0, 100, 500]
    --------------------------------------------------

    返回值:
      {
        "neutronics": { ... },
        "thermal_1d": { ... },
        "thermal_2d": { ... },
        "hydraulics": { ... },
        "control": { ... },
        "recorder": { ... },
        "visualization": { ... }
      }
    """

    ext = os.path.splitext(filepath)[1].lower()
    with open(filepath, 'r', encoding='utf-8') as f:
        if ext in ('.yaml', '.yml'):
            cfg = yaml.safe_load(f)
        elif ext == '.json':
            cfg = json.load(f)
        else:
            raise ValueError(f"Unsupported config format: {ext}")

    # 简单验证
    required_sections = [
        "neutronics", "thermal_1d", "thermal_2d",
        "hydraulics", "control", "recorder", "visualization"
    ]
    missing = [sec for sec in required_sections if sec not in cfg]
    if missing:
        raise KeyError(f"Input card missing sections: {missing}")

    return cfg
```

使用示例（`simulator.py` 顶部）：

```python
from core.input_parser import load_input_card

# 1. 读取配置
params = load_input_card("input_card.yaml")

# 2. 拆解子模块参数
neutronics_params    = params["neutronics"]
thermal1d_params     = params["thermal_1d"]
thermal2d_params     = params["thermal_2d"]
hydraulics_params    = params["hydraulics"]
control_params       = params["control"]
recorder_params      = params["recorder"]
visualization_params = params["visualization"]

# 3. 传给各模块
from core.neutronics import PointKineticsWithDecay
pk = PointKineticsWithDecay(**neutronics_params, dt=hydraulics_params["dt"])

from core.thermal_structure.one_d import solve_thermal_structure_1d
T_new = solve_thermal_structure_1d(**thermal1d_params, dx=hydraulics_params["dr"], dt=hydraulics_params["dt"], **thermal1d_params)

from core.hydraulics import update_hydraulics
rho, u, p, H = update_hydraulics(**hydraulics_params)

from controllers.manager import ControlManager
ctrl = ControlManager(dt=hydraulics_params["dt"])

from utils.data_recorder import DataRecorder
recorder = DataRecorder(output_dir=recorder_params["output_dir"])
```

这套 `load_input_card` 函数将配置集中在一个文件里，后续若要添加新模块或新参数，只需在 `input_card.yaml`/`.json` 中补充对应字段即可，无需修改 Python 代码，达成“一卡在手、全局可控”的灵活初始化。