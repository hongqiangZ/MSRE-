好嘞鸿强 ✅！我现在就为你逐个模块编写详细的接口文档，内容涵盖：

- 📦 模块概述与职责定位  
- 🧱 类与函数列表，包括方法签名、输入输出、用途说明  
- 🧪 关键物理公式与建模原理（如果适用）  
- 🛠️ 使用方式、调用示例、扩展建议

文档将统一采用 Markdown 格式放置于项目的 `docs/` 文件夹中，命名方式如下：

| 模块路径 | 文档文件名 |
|----------|------------|
| `core/neutronics.py` | `docs/core_neutronics.md` |
| `core/hydraulics.py` | `docs/core_hydraulics.md` |
| `thermal_structure/one_d.py` | `docs/thermal_one_d.md` |
| `controllers/control.py` & `manager.py` | `docs/controllers.md` |
| `utils/data_recorder.py` | `docs/utils_data_recorder.md` |
| `core/input_parser.py` | `docs/core_input_parser.md` |
| `core/io_interface.py` | `docs/core_io_interface.md` |
| `solver/tdma.py` | `docs/solver_tdma.md` |
| `utils/evaluator.py` | `docs/utils_evaluator.md` |

---

我先送上第一份：**core/neutronics.md**

## 📘 docs/core_neutronics.md

```markdown
# 核模块接口文档 — core/neutronics.py

## 🧠 模块职责

模拟点堆中子动力学行为，包括缓发中子群、功率响应与反应性反馈，核心类为 `PointKineticsWithDecay`。

---

## 🧱 类结构

### class `PointKineticsWithDecay`

用于描述延迟中子点堆动力学行为。

#### 🔧 初始化方法

```python
def __init__(self, beta_i, lambda_i, Lambda, T_c, tau, dt)
```

| 参数名 | 类型 | 描述 |
|--------|------|------|
| `beta_i` | list[float] | 每组缓发中子比例 |
| `lambda_i` | list[float] | 衰变常数 (1/s) |
| `Lambda` | float | 中子平均生命周期 |
| `T_c` | float | 核区驻留时间 |
| `tau` | float | 循环延迟时间 |
| `dt` | float | 时间步长 (s) |

---

## ⚛️ 模型物理公式

1. 中子功率变化：
   $$
   \frac{dn}{dt} = \frac{\rho - \beta}{\Lambda} n + \sum_{i} \lambda_i C_i
   $$

2. 缓发中子前体群变化：
   $$
   \frac{dC_i}{dt} = \frac{\beta_i}{\Lambda} n - \lambda_i C_i
   $$

3. 初始稳态浓度：
   $$
   C_i = \frac{\beta_i}{\Lambda \cdot \lambda_i}
   $$

---

### 🔁 方法

#### `step(rho: float) → Tuple[float, np.ndarray]`

推进一个时间步，返回新的功率 `n(t+dt)` 与前体浓度 `C(t+dt)`

---

## 🛠️ 使用示例

```python
pk = PointKineticsWithDecay(**neutronics_cfg, dt=0.5)
n, C = pk.step(rho=0.002)
```

---

## 🔄 状态变量

| 变量名 | 类型 | 描述 |
|--------|------|------|
| `self.n` | float | 当前中子功率（归一化） |
| `self.C` | np.ndarray | 每组前体浓度 |

---
```

---

如果你觉得满意，我将按此结构继续完成其余模块文档 ✍️📘。你是否想要我额外添加章节如「模型边界处理方式」「性能优化建议」或「常见错误与诊断」？我可以在每个模块末尾加入“开发者注释”板块。

下一份将是：`core/hydraulics.md` → 紧接着送上 🚀🧪