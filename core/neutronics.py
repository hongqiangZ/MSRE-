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


