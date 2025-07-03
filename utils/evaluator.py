import numpy as np

class ControlEvaluator:
    def __init__(self, t_list, response_list, ref_value, tolerance=0.01):
        self.t_list = np.array(t_list)
        self.y_list = np.array(response_list)
        self.ref = ref_value
        self.tol = tolerance

    def steady_state_error(self):
        last_vals = self.y_list[-10:]
        return float(np.mean(np.abs(last_vals - self.ref)))

    def overshoot(self):
        peak = np.max(self.y_list)
        return float((peak - self.ref) / self.ref * 100)

    def settling_time(self):
        for i in range(len(self.y_list)):
            if all(np.abs(self.y_list[i:] - self.ref) < self.tol * self.ref):
                return float(self.t_list[i])
        return None

    def rise_time(self):
        y_norm = (self.y_list - self.y_list[0]) / (self.ref - self.y_list[0])
        t_10 = next((t for t, y in zip(self.t_list, y_norm) if y >= 0.1), None)
        t_90 = next((t for t, y in zip(self.t_list, y_norm) if y >= 0.9), None)
        return float(t_90 - t_10) if t_10 and t_90 else None

    def report(self):
        return {
            "Steady-State Error": self.steady_state_error(),
            "Overshoot (%)": self.overshoot(),
            "Settling Time (s)": self.settling_time(),
            "Rise Time (s)": self.rise_time()
        }
