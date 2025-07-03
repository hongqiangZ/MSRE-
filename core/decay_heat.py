import numpy as np

class DecayHeatModel:
    """
    衰变热计算器，使用指数项拟合方法（文献式3.48）
    P_decay(t) = P0 * (A0 + A1·e^{-t/t1} + A2·e^{-t/t2} + A3·e^{-t/t3})
    """

    def __init__(self, A0, A1, A2, A3, t1, t2, t3):
        self.A0 = A0
        self.A1 = A1
        self.A2 = A2
        self.A3 = A3
        self.t1 = t1
        self.t2 = t2
        self.t3 = t3

    def compute(self, P0, t):
        """
        计算 t 秒时刻的衰变热功率

        参数：
        - P0: 停堆前的堆芯功率（W）
        - t: 停堆后经历的时间（秒）

        返回：
        - 衰变热功率（W）
        """
        A0, A1, A2, A3 = self.A0, self.A1, self.A2, self.A3
        t1, t2, t3 = self.t1, self.t2, self.t3

        return P0 * (A0 + A1 * np.exp(-t / t1) +
                     A2 * np.exp(-t / t2) +
                     A3 * np.exp(-t / t3))
