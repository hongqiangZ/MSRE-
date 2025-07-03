import os
import csv
import datetime

class SimulationLogger:
    """
    高级仿真日志器：记录数据、事件、控制行为、状态变化
    """

    def __init__(self, output_dir="outputs"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

        # 准备文件路径
        self.data_file = os.path.join(self.output_dir, "data_log.csv")
        self.event_file = os.path.join(self.output_dir, "event_log.txt")
        self.control_file = os.path.join(self.output_dir, "control_trace.csv")

        # 写入头
        with open(self.data_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Step", "Time(s)", "T_out(K)", "n", "rho", "U", "SCRAM"])
        with open(self.control_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Step", "Mode", "T_out", "Error_T", "U", "Error_n", "rho", "SCRAM"])
        with open(self.event_file, 'w') as f:
            f.write(f"=== Simulation Log Started at {datetime.datetime.now()} ===\n")

    def log_data(self, step, time_s, T_out, n, rho, U, scram):
        with open(self.data_file, 'a', newline='') as f:
            csv.writer(f).writerow([step, time_s, T_out, n, rho, U, int(scram)])

    def log_control(self, step, mode, error_T, U, error_n, rho, scram):
        with open(self.control_file, 'a', newline='') as f:
            csv.writer(f).writerow([step, mode, f"{T_out:.2f}", f"{error_T:.3f}", f"{U:.1f}", f"{error_n:.3f}", f"{rho:.5f}", int(scram)])

    def log_event(self, message):
        with open(self.event_file, 'a') as f:
            f.write(f"[{datetime.datetime.now()}] {message}\n")

    def finalize(self):
        with open(self.event_file, 'a') as f:
            f.write(f"=== Simulation Ended at {datetime.datetime.now()} ===\n")
