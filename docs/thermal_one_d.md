鸿强，我马上继续 💼✅！这轮我们进入：

## 🧯 docs/thermal_one_d.md — 一维热构件模块接口文档

```markdown
# 一维热构件模块接口文档 — thermal_structure/one_d.py

## 🧠 模块职责

使用一维 TDMA 算法求解热传导方程，模拟热构件在径向方向上的温度演化，包括边界条件处理和与控制器的温度反馈。

---

## 🔧 核心函数

### `solve_thermal_structure_1d(T, cfg, Q_source, dt)`

推进热构件温度场。

#### 参数说明：

| 参数名 | 类型 | 描述 |
|--------|------|------|
| `T` | list[float] | 当前温度分布（节点上） |
| `cfg` | dict | 热模块参数配置（来自 YAML） |
| `Q_source` | float | 当前热源项（如中子功率） |
| `dt` | float | 时间步长 |

#### 返回值：

```python
return T_new  # 更新后的温度分布
```

---

## 📦 重要配置字段（来自 YAML）

| 字段名 | 描述 |
|--------|------|
| `geometry` | 几何类型："cylinder", "cartesian" 等 |
| `init_temp` | 初始温度 |
| `k` | 导热系数 |
| `bc_type` | 边界条件类型，如 ["Dirichlet", "Robin"] |
| `bc_value` | 对应边界值，如 `[900, [100, 600]]` |

---

## 🔬 模型物理公式

1. 一维热传导方程：
   $$
   \frac{\partial T}{\partial t} = \frac{k}{\rho c_p} \frac{\partial^2 T}{\partial r^2} + \frac{Q_{\text{source}}}{\rho c_p}
   $$

2. Robin 边界条件（右侧对流）：
   $$
   -k \frac{\partial T}{\partial r} = h (T - T_\infty)
   $$

3. 隐式离散格式 → 三对角线性系统：
   $$
   A_i T_{i-1}^{n+1} + B_i T_i^{n+1} + C_i T_{i+1}^{n+1} = D_i
   $$

---

## 🧠 所用求解器

调用了 TDMA 求解器：

```python
from solver.tdma import solve_tridiagonal
```

使用三对角线矩阵求解隐式差分线性系统，适合高稳定性求解。

---

## 🛠️ 使用示例

```python
T_new = solve_thermal_structure_1d(
    T=T_old,
    cfg=thermal_cfg,
    Q_source=n * Fp,  # 中子功率 × 功率分布因子
    dt=0.5
)
```

---

## 📌 注意事项

- Robin 边界建议搭配对流模型温度；
- 对于非均匀网格或材料，还可扩展为二维 ADI；
- 与 `control.update()` 对接时，应使用出口温度 `T[-1]` 作为反馈指标；

---
```

---

下一份将是控制器模块文档：`docs/controllers.md`，会涵盖：

- `ControlManager` 如何调度不同控制器；
- `PIDController.update()` 的公式推导和限幅处理；
- SCRAM 逻辑的布尔触发机制；
- MPC 模块接口的占位说明与未来拓展建议。

马上开写 🔧🎮📘。是否你也想在控制文档中看到参数整定建议或典型响应行为的案例图？我可以在末尾加入一份“控制器性能调优参考”。你来定细节，我来继续构建。