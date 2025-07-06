太好了鸿强 ✅！我会继续按刚才的结构为每一个模块生成详细接口文档，确保内容清晰、准确，并融入必要的物理模型与使用示例。

下面是第二份文档：**流体动力学模块接口文档**

---

## 📘 docs/core_hydraulics.md

```markdown
# 流体动力学模块接口文档 — core/hydraulics.py

## 🧠 模块职责

模拟熔盐流体在回路中的运动与传热行为，包括密度、速度、压强、焓的时间演化，并与热构件模块耦合。

---

## 🔧 核心函数

### `update_hydraulics(rho_salt, u, p, H, T, dt, cfg)`

推进一个时间步的流体状态。

#### 输入参数：

| 参数名 | 类型 | 描述 |
|--------|------|------|
| `rho_salt` | float | 当前流体密度 |
| `u` | float | 当前流速 (m/s) |
| `p` | float | 当前压强 (Pa) |
| `H` | float | 当前焓值 |
| `T` | float | 当前温度 (K) |
| `dt` | float | 时间步长 (s) |
| `cfg` | dict | 水力模块配置参数，来源于 `input_card.yaml` |

#### 返回值：

```python
return rho_salt_new, u_new, p_new, H_new
```

---

## ⚙️ 模型参数与配置字段（来自 YAML）

| 字段名 | 说明 |
|--------|------|
| `g` | 重力加速度 |
| `friction` | 摩擦因子 |
| `A` | 管道截面积 |
| `Av` | 控制体积面积 |
| `rho_salt` | 熔盐初始密度 |
| `cp` | 比热容 |
| `p0` | 初始压强 |
| `u0` | 初始速度 |
| `H0` | 初始焓值 |
| `dr`, `dz` | 网格尺寸（可拓展为分布式解） |

---

## 🔬 模型公式（简化推导）

1. 连续性方程（质量守恒）：
   $$
   \frac{\partial \rho}{\partial t} + \rho \frac{\partial u}{\partial z} = 0
   $$

2. 动量方程（速度演化）：
   $$
   \rho \frac{du}{dt} = -\frac{dp}{dz} - f u^2 + \rho g
   $$

3. 能量方程（焓变化）：
   $$
   \rho c_p \frac{dT}{dt} = Q_{\text{heat}} - \text{losses}
   $$

4. 状态方程（简化理想熔盐）：
   $$
   p = f(\rho, T)
   $$

---

## 🛠️ 使用示例

```python
rho_salt, u, p, H = update_hydraulics(
    rho_salt=rho_salt, u=u, p=p, H=H,
    T=T[-1], dt=0.5, cfg=hydraulics_cfg
)
```

---

## 📌 注意事项

- 当前函数为单点耦合，可拓展为网格化 1D/2D 水力场；
- 与热构件模块温度 T 联动，用于更新密度与焓；
- 若需考虑流阻、泵功、进口/出口边界条件，可在 cfg 中设定扩展项。

---
```

---

下一份将是热构件模块：`docs/thermal_one_d.md`  
里面我会详细解析：

- `solve_thermal_structure_1d()` 的参数、矩阵构造逻辑；
- 如何实现边界条件（Dirichlet / Robin）；
- TDMA 三对角线性系统求解的物理含义；
- 示例图像或温度分布形态解释。

我马上开写，内容严谨又通俗 🧱🔥📘。你想文档里包含 TDMA 的算法图示或流程解释吗？我可以补图支持。继续前进 💼📊✍️。