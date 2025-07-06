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
