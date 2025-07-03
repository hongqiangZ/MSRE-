import numpy as np

class MPCController:
    """
    简易模型预测控制器接口（占位模板）
    用于未来集成线性 / 非线性 MPC，优化换热、流量、反应性等
    """

    def __init__(self, horizon=10, dt=1.0):
        self.horizon = horizon
        self.dt = dt
        self.ref = 0.0

    def update(self, state, ref=None):
        """
        输入当前状态和可选参考值，返回控制指令（如换热强度 U）

        state: dict，例如 {"T_out": 950, "n": 1.2}
        ref: 可选新目标
        """
        if ref is not None:
            self.ref = ref

        # ⚠️ 占位策略：线性预测 + P 控制（未来可替换为优化器）
        T = state.get("T_out", 900)
        error = T - self.ref
        U = max(0, 15000 - 500 * error)  # 仅作占位演示
        return U
