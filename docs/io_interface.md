当然鸿强 ✅！这份是第七份模块文档，介绍 MSREⅡ 的外部程序接口模块，它实现了与其他系统的数据交互：读取输入、导出结果、Socket通信等功能。你可以用它实现远程操控仿真，或接入外部数据库与优化算法。

---

## 📘 docs/core_io_interface.md — 外部接口模块接口文档

```markdown
# 外部接口模块接口文档 — core/io_interface.py

## 🧠 模块职责

实现 MSREⅡ 与外部系统之间的数据交互，包括：

- 从 JSON 文件读取控制参数或仿真配置；
- 将仿真结果写入 CSV；
- 向 Socket 端口发送仿真状态数据，支持远程联控或仪表集成。

---

## 🔧 核心函数一览

### `read_input_json(filepath: str) → dict`

从指定路径读取 JSON 文件作为仿真输入或控制器设定参数。

#### 示例：

```python
config = read_input_json("external_input.json")
```

---

### `write_output_csv(data: dict, filepath: str)`

将仿真结果以字典格式写入 CSV 文件。

#### 示例：

```python
write_output_csv(
    {"T_out": 943.2, "n": 1.12, "rho": 0.003},
    "outputs/run1/result.csv"
)
```

---

### `send_to_socket(ip: str, port: int, payload: dict)`

通过 TCP Socket 将仿真状态发送给指定服务器，适用于仪表板显示、实时接口联动、IoT集成。

#### 示例：

```python
send_to_socket("127.0.0.1", 5050, {"step": 20, "T_out": 944.0})
```

---

## 📡 Socket 通信格式建议

- 使用 JSON 字符串作为通信内容；
- 每次发送内容格式如下：

```json
{
  "step": 40,
  "n": 1.22,
  "T_out": 946.5,
  "U": 10800,
  "SCRAM": false
}
```

- 建议使用 UTF-8 编码，结尾使用换行符 `\n` 进行包分隔。

---

## 🛠️ 使用场景建议

| 应用场景 | 建议功能 |
|----------|-----------|
| 优化算法调度 | 通过 Socket 将仿真输出发送给优化器进行迭代 |
| 仿真仪表板 | 与 GUI 前端联动，显示实时结果 |
| 多任务管理 | 从 JSON 配置文件加载多组仿真参数轮询执行 |
| REST API 联动 | 与 `api_server.py` 配合，实现远程控制与结果查询 |

---

## 📌 注意事项

- 建议对 JSON 输入进行字段完整性检查，避免仿真初始化失败；
- Socket 通信建议设置超时机制与重连策略；
- 可拓展为 WebSocket 或 HTTP 接口与网页系统集成。

```

---

下一份将是 TDMA 求解器模块接口文档 `docs/solver_tdma.md`，内容包括：

- 三对角矩阵求解算法实现；
- 离散格式公式与数值稳定性；
- 与热传导模块的耦合方式；
- 边界条件如何嵌入系数矩阵。

我会继续保持高质量输出 💡🧱📘。是否你也想在 TDMA 文档末尾补充一个数值稳定性分析与 CFL 条件参考？我可以一并加上。马上启动下一份构建。