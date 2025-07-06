鸿强，我们继续推进 ✅！下面是第四份文档：

## 🎮 docs/controllers.md — 控制器模块接口文档

```markdown
# 控制器模块接口文档 — controllers/

## 🧠 模块职责

调度并执行反应堆控制行为，包括 PID 控制器、SCRAM 故障处理器、MPC 模拟器等，通过 `ControlManager` 实现集中式调用。

---

## 📂 模块文件结构

- `control.py`：增量式 PID 控制器
- `logic.py`：布尔逻辑控制（SCRAM）
- `mpc.py`：MPC 控制器占位
- `manager.py`：控制器调度器（ControlManager）

---

## 🎮 核心类结构

### class `ControlManager`

#### 初始化方法

```python
def __init__(self, cfg: dict)
```

| 参数名 | 描述 |
|--------|------|
| `cfg` | 来自 YAML 的控制器配置字典（包含目标值与控制器参数） |

---

### 🔁 主控制方法

#### `update(T_out: float, n: float) → Tuple[float, float]`

根据当前出口温度与功率，输出新的反应性 ρ 与控制量 U。

返回值：

```python
rho, U = control.update(T_out, n)
```

---

## 🧪 PID 控制器（control.py）

### class `PIDController`

#### 初始化方法

```python
def __init__(Kp, Ti, Td, limits)
```

#### 更新方法

```python
def update(error, dt)
```

计算响应值：

$$
u(t) = K_p \left( e(t) + \frac{1}{T_i} \int e(t) dt + T_d \frac{de(t)}{dt} \right)
$$

并限制在预设范围 `[min, max]`

---

## 💡 SCRAM 逻辑模块（logic.py）

### `scram_check(T_out, n) → bool`

根据功率或温度异常触发 SCRAM

### `switch_mode(state, faults) → str`

切换控制模式，例如：

- 正常 → SCRAM
- PID → MPC（未来拓展）

---

## 🧠 MPC 模块（mpc.py）

### class `MPCController`（占位）

模拟未来行为，优化目标函数，例如：

$$
\min \sum_{t=0}^{H} (T_t - T_{\text{ref}})^2 + \lambda U_t^2
$$

可拓展为调用 `cvxpy` 求解器

---

## 🛠️ 使用示例

```python
control = ControlManager(control_cfg)
rho, U = control.update(T_out=T[-1], n=n)
```

---

## 📌 注意事项

- 控制器可接入多个输入信号（多变量控制）
- SCRAM 逻辑建议使用 `flag: True/False` 控制中断
- MPC 模块建议使用真实约束和动态模型构建求解器
```

---

下一份将是 `docs/utils_data_recorder.md`，分析：

- 如何使用 `record_scalar()` 和 `record_array()`；
- 输出为 CSV 和 NPY 的逻辑；
- 数据结构设计思路与扩展接口。

是否你希望我也在末尾附加一个“字段命名建议表”，规范 `scalars.csv` 与数据记录结构？我可以立刻一并加上 ✍️📊🧠。马上继续送上下一份文档！