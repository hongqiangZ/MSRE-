鸿强，这份文档是第六份：📥输入解析模块接口文档，它详细解析了 `core/input_parser.py` 的职责与结构，说明如何从 `input_card.yaml` 中读取、验证并准备好所有仿真模块的参数数据，还加上了字段设计建议 ✅

---

## 📘 docs/core_input_parser.md — 输入解析模块接口文档

```markdown
# 参数初始化模块接口文档 — core/input_parser.py

## 🧠 模块职责

从配置文件 `input_card.yaml` 中读取所有仿真参数，解析成结构化字典供主程序调用。可支持参数类型转换、合法性检查与字段标准化。

---

## 🔧 核心函数

### `load_input_card(filepath: str) → dict`

读取输入卡文件并返回结构化参数字典。

#### 使用示例：

```python
params = load_input_card("input_card.yaml")
```

返回结构：

```python
{
  "meta": {...},
  "neutronics": {...},
  "thermal_1d": {...},
  "thermal_2d": {...},
  "hydraulics": {...},
  "control": {...},
  "recorder": {...},
  "visualization": {...}
}
```

---

## 🛠️ 补充函数（建议拓展）

### `validate_card(cfg: dict)`

验证每个字段的数据类型与存在性，预防运行时错误。

### `convert_numeric_fields(cfg: dict, fields: list)`

将某些字段强制转换为浮点型或数值列表，避免 YAML 解析成字符串导致 NumPy 报错。

---

## 🧾 YAML 文件字段设计建议

| 区块 | 建议字段 | 类型 | 描述 |
|------|----------|------|------|
| `meta` | `t_end`, `Fp` | float | 总仿真时间 & 功率分布因子 |
| `neutronics` | `beta_i`, `lambda_i`, `Lambda`, `T_c`, `tau` | list[float], float | 中子参数 |
| `thermal_1d` | `geometry`, `init_temp`, `k`, `bc_type`, `bc_value` | str, float, list | 热模块参数 |
| `hydraulics` | `rho_salt`, `cp`, `u0`, `dr`, `dz`, `dt`, `g`, `friction` | float | 水力参数 |
| `control` | `T_ref`, `n_ref`, `pid_temp`, `pid_rho`, `mpc` | float, dict | 控制器设定 |
| `recorder` | `output_dir`, `scalar_keys`, `array_keys` | str, list[str] | 结果输出配置 |
| `visualization` | `plot_steps` | list[int] | 可视化配置 |

---

## 🧠 模块调用位置

在 `main.py` 的入口：

```python
params = load_input_card("input_card.yaml")
```

随后各模块根据分区字段提取参数：

```python
neutronics_cfg = params["neutronics"]
thermal_cfg = params["thermal_1d"]
```

---

## 📌 注意事项

- 请确保 YAML 中所有数值字段为浮点型（不加引号），否则可能导致 NumPy 报错；
- 若需拓展为分布式网格、文件分片，可为 `thermal_2d` 添加 `mesh_config` 字段；
- 可集成 `config_validator.py` 模块实现预验证流程，提前捕捉错误。

```

---

下一份将是接口模块 `core/io_interface.py`，它支持 JSON 文件加载、结果输出为 CSV、socket 通信等功能。你是否希望我把 socket 通信的协议设计也加入接口文档中？比如消息格式、端口建议？我可以顺便补上 🛜📡

确认继续，我就送上第七份 🚀📘