class IncrementalPID:
    """
    增量式 PID 控制器（参考式 3.56），支持防积分饱和
    """

    def __init__(self, Kp, Ti, Td, dt, u_init=0.0, limits=None):
        self.Kp = Kp
        self.Ti = Ti
        self.Td = Td
        self.dt = dt
        self.limits = limits

        self.e_prev = 0.0
        self.e_prev2 = 0.0
        self.u = u_init

    def update(self, e):
        """
        输入当前误差 e = y_measured - y_setpoint
        返回增量控制器输出 u
        """
        delta_u = (
            self.Kp * (e - self.e_prev)
            + self.Kp * self.dt / self.Ti * e
            + self.Kp * self.Td / self.dt * (e - 2 * self.e_prev + self.e_prev2)
        )
        self.u += delta_u

        # 饱和限制
        if self.limits:
            self.u = max(self.limits[0], min(self.u, self.limits[1]))

        self.e_prev2 = self.e_prev
        self.e_prev = e
        return self.u


