当然鸿强 ✅！这份是第九份模块文档，专注于控制器性能评估模块 `utils/evaluator.py`，它帮助你将控制响应从“感觉不错”转化为“指标明确”，并补充了你特别要求的“响应分类说明”。

---

## 📘 docs/utils_evaluator.md — 控制器性能评估模块接口文档

```markdown
# 控制器性能评估模块接口文档 — utils/evaluator.py

## 🧠 模块职责

分析控制器响应行为，量化其性能指标，包括稳态误差、响应时间、超调率等，用于比较不同控制策略（如 PID vs MPC）或调参优化参考。

---

## 📦 类结构

### class `ControlEvaluator`

初始化评估器：

```python
def __init__(self, t_list, response_list, ref_value)
```

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `t_list` | list[float] | 仿真时间序列 |
| `response_list` | list[float] | 控制目标变量值，如 `T_out` |
| `ref_value` | float | 目标设定值，如 `T_ref` |

---

## 📊 核心方法

### `steady_state_error() → float`

输出最终稳态误差：

$$
e_{ss} = |T_{\text{final}} - T_{\text{ref}}|
$$

---

### `overshoot_percent() → float`

最大超调百分比：

$$
\text{Overshoot} = \frac{T_{\text{peak}} - T_{\text{ref}}}{T_{\text{ref}}} \times 100\%
$$

---

### `settling_time(threshold=2%) → float`

系统进入±阈值范围并保持不变的时间。

### `rise_time() → float`

响应从10% 到90% 的时间段。

---

### `report() → dict`

综合输出所有指标：

```python
{
  "Steady-State Error": 2.73,
  "Overshoot (%)": 5.20,
  "Settling Time (s)": 35.0,
  "Rise Time (s)": 15.0
}
```

---

## 📈 控制响应分类说明

| 分类 | 特征 | 表现行为 |
|------|------|-----------|
| 欠调节 Underdamped | 响应太慢，稳态误差高 | 控制器作用不够，设定点无法及时达到 |
| 过调节 Overdamped | 响应过快、振荡剧烈 | 控制器作用过强，超调大，可能不稳定 |
| 临界调节 Critically Damped | 响应快速、稳态稳 | 最佳响应状态，误差小，能迅速达到目标 |

你可通过超调率和稳态误差判断控制器属于哪个类别，并据此调整 `Kp`, `Ti`, `Td`。

---

## 🛠️ 使用示例

```python
evaluator = ControlEvaluator(t_list, T_out_list, T_ref)
results = evaluator.report()
for k, v in results.items():
    print(f"{k}: {v:.2f}")
```

---

## 📌 推荐阈值参考（PID 控制）

| 指标 | 推荐值区间 |
|------|------------|
| Steady-State Error | < 2.0 |
| Overshoot (%) | < 10% |
| Settling Time | < 60s |
| Rise Time | < 30s |

---

## 📌 注意事项

- 若响应数据过于震荡，可先进行平滑处理；
- 对于多变量控制器，可分别评估每个通道的响应；
- 支持扩展为图像分析，例如标记响应关键点、绘图等。

```

---

下一份将是压轴篇：**README.md 与 `docs/index.md` 聚合说明文档**，我会整合你所有模块文档，让新用户或将来的你能轻松浏览项目结构、模块职责、使用方式、接口规范。

同时我也能为你生成控制器调参助手、性能评估图生成器，甚至“自动报告构建器”将仿真结果汇总为 PDF 📊📘。

你来定终章节奏，我全力部署 🔧📚🚀。是否我们开始写 `docs/index.md`，或你还想给 GUI 或 REST API 单独一章？我也可以为这些模块补文档。说一声我就动手。