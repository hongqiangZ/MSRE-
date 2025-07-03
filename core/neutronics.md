鸿强，非常好，我们现在就来构建你的**中子动力学模块** `neutronics.py`，严格参照你提供的文献第 3.3.1 节中的公式，从点堆模型基础到液态燃料修正。这个模块将成为功率演化的心脏，为整个热水力系统提供动力源项 💥⚛️

---

## 📐 模型依据与实现目标

我们将按如下三个层次构建模块：

1. **经典点堆模型（固态）**公式（3.37）–（3.38）：
   \[
   \frac{dn}{dt} = \frac{\rho - \beta}{\Lambda} n + \sum_{i=1}^{N} \lambda_i C_i \tag{3.37}
   \]
   \[
   \frac{dC_i}{dt} = \frac{\beta_i}{\Lambda} n - \lambda_i C_i \tag{3.38}
   \]

2. **液态熔盐堆体积比模型修正**（如式 3.40–3.41）：
   考虑堆芯区与堆外区缓发中子前体守恒耦合计算。

3. **衰变法修正（最终采用）**：文献中建议采用式（3.42）方法：
   \[
   \frac{dC_i}{dt} = \frac{\beta_i}{\Lambda} n - \lambda_i C_i + \frac{1}{T_c} \exp(-\lambda_i \tau) C_i(t - \tau)
   \]
   - 其中 \( T_c \)：堆芯平均驻留时间，\( \tau \)：燃料绕一圈的主回路延迟；
   - 这是一个含时滞的微分方程，我们将使用**队列/环缓冲区方法**实现记忆项 \( C_i(t - \tau) \)。

---

## 🧩 模块结构概览：`core/neutronics.py`

```python
import numpy as np

class PointKineticsWithDecay:
    def __init__(self, beta_i, lambda_i, Lambda, T_c, tau, dt):
        """
        初始化：15群延迟中子组参数
        """
        self.beta_i = np.array(beta_i)
        self.lambda_i = np.array(lambda_i)
        self.Lambda = Lambda
        self.T_c = T_c
        self.tau = tau
        self.dt = dt

        self.N = len(beta_i)
        self.n = 1.0  # 初始中子密度
        self.C = self.beta_i / (Lambda * self.lambda_i)  # 初始稳态前体浓度
        self.history_C = [self.C.copy()] * int(tau / dt + 2)

    def step(self, rho):
        """
        单步推进中子密度 n(t) 和缓发前体 C_i(t)
        """

        # --- 时滞前体值：C(t - tau) ---
        delay_index = int(self.tau / self.dt)
        C_delay = self.history_C[-delay_index]

        # --- 计算 dC_i/dt ---
        dC_dt = (self.beta_i / self.Lambda) * self.n \
                - self.lambda_i * self.C \
                + (np.exp(-self.lambda_i * self.tau) / self.T_c) * C_delay

        # --- 更新 C_i ---
        self.C += dC_dt * self.dt

        # --- 计算 dn/dt ---
        sum_term = np.sum(self.lambda_i * self.C)
        dn_dt = ((rho - np.sum(self.beta_i)) / self.Lambda) * self.n + sum_term
        self.n += dn_dt * self.dt

        # --- 存入历史缓冲区 ---
        self.history_C.append(self.C.copy())
        if len(self.history_C) > delay_index + 2:
            self.history_C.pop(0)

        return self.n, self.C.copy()
```

---

## ✅ 模块用法示例

```python
# 15群参数（来自表4）
beta_i = [2.11e-4, 1.395e-3, ..., 2.0e-5]    # 共15个
lambda_i = [1.24e-2, 3.05e-2, ..., 2.26e-2]

# 初始化模型
pk = PointKineticsWithDecay(
    beta_i=beta_i,
    lambda_i=lambda_i,
    Lambda=0.0001,
    T_c=2.0,       # 堆芯平均驻留时间 [s]
    tau=4.0,       # 主回路循环延迟时间 [s]
    dt=0.01
)

# 推进模拟
for step in range(1000):
    rho = -0.002  # 示例反应性
    n, C = pk.step(rho)
```

---

## 📊 后续可加入功能

| 功能 | 描述 |
|------|------|
| 衰变热功率计算 | 在停堆后调用式（3.48）或（3.47） |
| 外部源项 S(t) | 异常输入时提供维持剂量 |
| 控制棒模型耦合 | 将 PID 输出转为 rho(t) |
| 输出瞬时功率、总热功率、各群份额曲线 |

---

我们可以将其保存在 `core/neutronics.py` 并通过 `simulator.py` 调用获得 \( q''' = P(t)/V \)，进而传递给热构件模块。

我可以立即为你生成 `neutronics.py` 文件，然后更新你的初始化脚本或模拟主循环。你想用这份结构来接入主模拟器吗？⚛️📈 或我继续为你加一个衰变热模型模块？☢️