from controllers.pid import IncrementalPID
from controllers.logic import BooleanController
from controllers.mpc import MPCController

class ControlManager:
    def __init__(self, dt):
        self.dt = dt

        # 控制器初始化
        self.pid_temp = IncrementalPID(Kp=2000, Ti=50, Td=300, dt=dt, limits=(1000, 20000))
        self.pid_rho = IncrementalPID(Kp=500, Ti=100, Td=10, dt=dt, limits=(-0.01, 0.01))
        self.mpc_U = MPCController(horizon=10, dt=dt)

        self.scram_logic = BooleanController(threshold=1200, mode='greater')  # SCRAM触发温度

        self.control_mode = 'pid'  # 默认使用 PID
        self.log = []

    def update(self, sensors: dict, step: int):
        """
        主控制接口
        - sensors: {"T_out": ..., "n": ..., "T_ref": ..., "n_ref": ...}
        - step: 当前仿真步，用于日志
        返回：
        - {"U": ..., "rho": ..., "scram": ...}
        """
        T_out = sensors.get("T_out", 900)
        T_ref = sensors.get("T_ref", 900)
        n = sensors.get("n", 1.0)
        n_ref = sensors.get("n_ref", 1.0)

        # 1️⃣ SCRAM 判断
        scram = self.scram_logic.update(T_out)
        if scram:
            rho = -0.01
            self.log.append(f"[Step {step}] ⚠️ SCRAM triggered → T_out={T_out:.2f}K → ρ=-0.01")
        else:
            error_n = n - n_ref
            rho = self.pid_rho.update(error_n)

        # 2️⃣ 控制换热器传热能力（U）
        try:
            if self.control_mode == 'pid':
                error_T = T_out - T_ref
                U = self.pid_temp.update(error_T)

                # 故障识别（输出震荡或超幅度变化）
                if abs(U - self.pid_temp.u) > 1000:
                    self.log.append(f"[Step {step}] ⚠️ PID anomaly detected, switching to MPC mode.")
                    self.control_mode = 'mpc'

            elif self.control_mode == 'mpc':
                U = self.mpc_U.update(sensors, ref=T_ref)

            else:
                U = 15000  # fallback 值

        except Exception as e:
            U = 15000
            self.log.append(f"[Step {step}] ❗ Control update error: {e} → fallback U=15000")

        # 3️⃣ 日志输出
        self.log.append(
            f"[Step {step}] Mode={self.control_mode}, T_out={T_out:.1f}, U={U:.1f}, ρ={'SCRAM' if scram else f'{rho:.5f}'}"
        )

        return {"U": U, "rho": rho, "scram": scram}

    def export_log(self, filepath="control_log.txt"):
        """
        导出日志到文件
        """
        with open(filepath, 'w', encoding='utf-8') as f:
            for line in self.log:
                f.write(line + '\n')
