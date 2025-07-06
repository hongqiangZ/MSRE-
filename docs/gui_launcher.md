当然鸿强 ✅！我来为 MSREⅡ 项目补上最后两章模块接口文档，分别是 GUI 启动器与 REST API 服务，它们是用户交互与远程控制的入口模块，也是系统从研究型仿真向平台化应用迈进的重要桥梁 🌐🖥️

---

## 📘 docs/gui_launcher.md — 图形启动器接口文档（GUI模块）

```markdown
# 图形启动器模块接口文档 — gui_launcher.py

## 🧠 模块职责

使用 Streamlit 构建图形化用户界面，提供仿真参数选择、模型运行按钮、结果展示与曲线绘图功能，便于非技术用户快速使用仿真平台。

---

## 🧪 核心功能结构

1. 📥 加载配置参数 `input_card.yaml`
2. 🎛️ 提供参数调整面板（如初始温度、控制器选型）
3. ▶️ 启动仿真主函数 `main.py`
4. 📊 展示仿真结果：温度曲线、中子功率、控制响应等
5. 📎 下载结果数据：CSV、NPY

---

## 🔧 推荐使用方式

在终端运行：

```bash
streamlit run gui_launcher.py
```

或者双击执行，启动浏览器页面。

---

## 📊 图像展示模块建议

- 使用 `matplotlib` 绘制时间序列图；
- 支持下拉切换变量，如 `T_out`, `rho`, `n`;
- 支持热场动态动画（配合 NPY 文件）

---

## 📌 注意事项

- 确保 outputs/run1/ 已存在数据文件；
- 若前一次仿真未完成，可添加异常提示模块；
- 可拓展为多仿真任务批处理界面；
```

---

## 📘 docs/api_server.md — REST API 接口模块文档

```markdown
# REST 接口模块文档 — api_server.py

## 🧠 模块职责

提供远程调用 MSREⅡ 仿真的服务接口，支持前端网页或外部程序通过 HTTP 请求传入参数，启动仿真，获取输出结果并返回。

---

## 🚀 核心 API 路由建议

| 路径 | 方法 | 功能说明 |
|------|------|----------|
| `/run_simulation` | POST | 运行仿真主流程，接收配置数据 JSON |
| `/get_result` | GET | 返回最近一次仿真结果 |
| `/status` | GET | 查询仿真运行状态 |
| `/download` | GET | 提供结果数据打包下载（ZIP/CSV）

---

## 🧪 示例调用方式（使用 `requests` 库）

```python
import requests
response = requests.post("http://localhost:8000/run_simulation", json=input_cfg)
print(response.json())
```

---

## 🛡️ 输入结构建议（JSON）

```json
{
  "T_ref": 950,
  "initial_temp": 900,
  "control_type": "PID",
  "duration": 300
}
```

---

## 📂 输出数据格式

返回结构体：

```json
{
  "time": [0, 10, 20],
  "T_out": [900, 920, 950],
  "n": [1.0, 1.1, 1.2],
  "rho": [0.0, 0.003, 0.006],
  "status": "completed"
}
```

---

## 📌 注意事项

- 建议运行时异步处理长流程，避免阻塞；
- 返回结果建议带上仿真 ID，可用于查询与下载；
- 可拓展为接收文件上传（如 input_card.yaml）

---
```

---

✅ 所有模块文档已覆盖完成，鸿强，你已经搭建起一个科研级可控熔盐堆仿真平台，具备高度模块化、控制闭环、数据分析、前后端交互能力！

是否我们现在开始汇总 `docs/index.md` 主文档，用于整合所有说明并作为 GitHub 或发布项目的总入口？也可以开始生成控制器调参助手或自动报告生成器模块。你来定主线，我继续推进📘🚀🔧