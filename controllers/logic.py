class BooleanController:
    """
    简单布尔控制器：根据某个物理变量是否超出阈值激活或关闭模块
    例如：T > T_trip → SCRAM，或 流量 < Q_min → 关闭换热
    """

    def __init__(self, threshold, mode='greater', hold_state=True):
        self.threshold = threshold
        self.mode = mode
        self.hold_state = hold_state
        self.active = False

    def update(self, value):
        """
        输入当前变量值，输出激活状态 True/False
        """
        if self.mode == 'greater' and value > self.threshold:
            self.active = True
        elif self.mode == 'less' and value < self.threshold:
            self.active = True
        elif not self.hold_state:
            self.active = False
        return self.active
