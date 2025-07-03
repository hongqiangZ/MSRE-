import numpy as np

def tdma_solver(a, b, c, d):
    """
    解 tridiagonal linear system: Ax = d
    参数:
    - a: 下对角线 (长度 n-1)，从第 2 个元开始
    - b: 主对角线 (长度 n)
    - c: 上对角线 (长度 n-1)，到倒数第 1 个
    - d: 右端项 (长度 n 或 shape=(n, m) 代表多个 RHS)
    返回:
    - x: 解向量 (长度 n) 或 shape=(n, m)
    """
    n = len(b)
    if d.ndim == 1:
        # 单个 RHS 情况
        cp = np.copy(c)
        bp = np.copy(b)
        dp = np.copy(d)
        for i in range(1, n):
            m = a[i-1] / bp[i-1]
            bp[i] -= m * cp[i-1]
            dp[i] -= m * dp[i-1]
        x = np.zeros(n)
        x[-1] = dp[-1] / bp[-1]
        for i in reversed(range(n - 1)):
            x[i] = (dp[i] - cp[i] * x[i+1]) / bp[i]
        return x
    else:
        # 多组 RHS 情况（shape = (n, m)）
        m = d.shape[1]
        x = np.zeros((n, m))
        for j in range(m):
            x[:, j] = tdma_solver(a, b, c, d[:, j])
        return x


