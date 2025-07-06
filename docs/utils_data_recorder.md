当然鸿强 ✅！这份文档将是你的第五份接口说明文档，涵盖数据记录模块的结构与设计理念，同时我也附上字段命名建议表，帮助你确保输出数据在后续分析中具有一致性与可读性。

---

## 📘 docs/utils_data_recorder.md — 数据记录器模块接口文档

```markdown
# 数据记录模块接口文档 — utils/data_recorder.py

## 🧠 模块职责

负责在每个仿真时间步记录关键物理量，包括标量值（如功率、温度）与数组场（如温度分布），并在仿真结束后统一导出为 CSV 与 NPY 格式，供分析与可视化使用。

---

## 📂 类结构

### class `DataRecorder`

#### 初始化方法

```python
def __init__(self, cfg: dict)
```

| 参数 | 描述 |
|------|------|
| `cfg` | 配置字典，包含输出路径与记录字段信息，如 `scalar_keys` 和 `array_keys` |

---

## 📦 核心方法

### `record_scalar(key: str, value: float)`

记录一个时间步的标量变量。

### `record_array(key: str, arr: list | np.ndarray)`

记录一个时间步的数组字段（如温度分布）。

### `export_all()`

在仿真结束时将所有记录数据输出为：

- `scalars.csv`
- `T_core.npy` / `T_field.npy`（根据配置字段）

---

## 📁 文件输出结构（示例）

```
outputs/run1/
├── scalars.csv        # 时间序列数据
├── T_core.npy         # 一维温度分布
├── T_field.npy        # 二维热场（如有）
├── control_trace.csv  # 控制器响应记录
├── event_log.txt      # 控制行为日志
```

---

## 🧪 字段命名建议表

| 字段名 | 推荐类型 | 描述 |
|--------|------------|------|
| `time` | float | 当前仿真时间 |
| `n` | float | 中子功率（归一化） |
| `T_out` | float | 热构件出口温度 |
| `rho` | float | 反应性值 |
| `U` | float | 控制器输出值（如热功率设定） |
| `T_core` | np.ndarray | 堆芯温度分布（一维） |
| `T_field` | np.ndarray | 热场二维分布（如二维模型） |
| `C_i` | list[float] | 缓发前体浓度组（可选） |
| `SCRAM_flag` | bool | SCRAM 触发状态 |

> 建议所有标量字段统一记录在 `scalars.csv`，数组字段使用 `.npy` 保存，更适合后处理与可视化。

---

## 🛠️ 使用示例

```python
recorder = DataRecorder(cfg)

recorder.record_scalar("T_out", T[-1])
recorder.record_scalar("n", n)
recorder.record_array("T_core", T)

# 仿真结束
recorder.export_all()
```

---

## 📌 注意事项

- 建议在初始化时动态检查 `scalar_keys` 与 `array_keys` 是否匹配仿真变量；
- 对于二维热场或多个数组字段，应在 `array_keys` 中标明命名，避免冲突；
- 可与日志记录器协同使用，以实现事件驱动数据标记。

```

---

下一份将是输入解析模块文档：**`docs/core_input_parser.md`**  
我会详述 `load_input_card()` 的解析逻辑、类型处理策略，以及如何设计可扩展的 YAML 文件结构。

想不想我顺便写一个字段类型验证机制？例如每组值都要是 float 或 list[float]，可提前捕捉配置错误。你来定义深度，我继续向下构建 📘🧠🧩。马上开始下一份编写。