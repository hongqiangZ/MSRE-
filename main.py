# main.py
from core.input_parser import load_input_card
from core.neutronics import PointKineticsWithDecay
from core.thermal_structure.one_d import solve_thermal_structure_1d
from core.hydraulics import update_hydraulics
from controllers.manager import ControlManager
from utils.data_recorder import DataRecorder
from utils.logger import SimulationLogger

import numpy as np
import os

def main():
    # === 1. 读取配置文件 ===
    params = load_input_card("input_card.yaml")
    neutronics_cfg    = params['neutronics']
    thermal1d_cfg     = params['thermal_1d']
    hydraulics_cfg    = params['hydraulics']
    control_cfg       = params['control']
    recorder_cfg      = params['recorder']

    dt = hydraulics_cfg['dt']
    steps = int(params['meta']['t_end'] / dt)

    # === 2. 初始化各模块 ===
    pk = PointKineticsWithDecay(**neutronics_cfg, dt=dt)

    N = hydraulics_cfg['N']
    dx = hydraulics_cfg['dr']
    x = np.linspace(0, N*dx, N)
    T = np.ones(N) * thermal1d_cfg.get('init_temp', 900)
    rho_f = np.ones(N) * hydraulics_cfg.get('rho_salt', 1800)
    cp_f  = np.ones(N) * hydraulics_cfg.get('cp', 1500)
    k_f   = np.ones(N) * thermal1d_cfg.get('k', 10)
    q     = np.zeros(N)

    u = np.ones(N) * hydraulics_cfg.get('u0', 1.0)
    p = np.ones(N) * hydraulics_cfg.get('p0', 1e5)
    H = np.ones(N) * hydraulics_cfg.get('H0', 2e5)

    ctrl = ControlManager(dt=dt)
    recorder = DataRecorder(recorder_cfg['output_dir'])
    logger = SimulationLogger(recorder_cfg['output_dir'])

    # === 3. 开始时间推进循环 ===
    for step in range(steps):
        t = step * dt

        # 控制器输入
        sensors = {
            'T_out': T[-1],
            'T_ref': params['control'].get('T_ref', 950),
            'n': pk.n,
            'n_ref': params['control'].get('n_ref', 1.0)
        }
        actions = ctrl.update(sensors, step)
        U = actions['U']
        rho = actions['rho']
        scram = actions['scram']
        if scram:
            rho = -0.01

        # === 中子动力学 ===
        n, C = pk.step(rho)

        # === 功率密度计算 ===
        P0 = n  # 假设归一化
        q[:] = P0 * params['meta'].get('Fp', 1.0)  # 简化功率分布

        # === 热工结构计算 ===
        T = solve_thermal_structure_1d(
            T=T, k=k_f, rho=rho_f, cp=cp_f, q=q,
            dx=dx, dt=dt,
            geometry=thermal1d_cfg['geometry'],
            bc_type=thermal1d_cfg['bc_type'],
            bc_value=thermal1d_cfg['bc_value']
        )

        # === 流体动力学计算 ===
        rho_f, u, p, H = update_hydraulics(rho_f, u, p, H, dx=dx, dt=dt, **hydraulics_cfg)

        # === 数据记录 ===
        recorder.record_scalar("time", t)
        recorder.record_scalar("n", n)
        recorder.record_scalar("T_out", T[-1])
        recorder.record_scalar("rho", rho)
        recorder.record_scalar("U", U)
        recorder.record_scalar("scram", scram)
        recorder.record_array("T_core", T)

        logger.log_data(step, t, T[-1], n, rho, U, scram)

    # === 4. 输出结果 ===
    recorder.export_scalars()
    recorder.export_arrays()
    logger.finalize()

    print("✅ 模拟完成。输出数据保存在:", recorder_cfg['output_dir'])


        # ✅ 添加在 main() 函数的最后
    from utils.evaluator import ControlEvaluator

    T_ref = params['control']['T_ref']
    t_hist = [dt * i for i in range(steps)]
    T_out_list = recorder.scalar_data.get("T_out", [])

    evaluator = ControlEvaluator(t_hist, T_out_list, T_ref)
    report = evaluator.report()

    print("\n📈 控制器性能评估结果：")
    for key, val in report.items():
        print(f"{key}: {val:.3f}")
# main.py


if __name__ == "__main__":
    main()
