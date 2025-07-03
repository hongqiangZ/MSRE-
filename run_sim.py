# File: run_sim.py
# 路径：run_sim.py
import os

# 跳转工作目录
os.chdir(os.path.dirname(__file__))

# 执行主循环
from main import main
main()
