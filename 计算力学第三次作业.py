import numpy as np
import matplotlib.pyplot as plt

# 解决中文显示问题
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# ----------------------
# 1. 准备数据（匹配原图趋势与交点）
# ----------------------
# 离散单元数量 n (对数刻度分布)
n = np.array([5, 10, 20, 40, 80, 160, 320, 640, 1000])

# 实际收敛误差（蓝色曲线，初始值更高，与红色线在n≈10处相交）
error_actual = np.array([0.3, 0.09, 0.022, 0.0055, 0.0014, 0.00035, 0.00008, 0.00002, 0.000005])

# 理论1阶收敛参考线（红色虚线，斜率=-1，与蓝色线在n≈10处相交）
n_ref = np.array([5, 1000])
error_ref = np.array([0.12, 0.0006])  # 斜率=-1，log-log下为直线

# ----------------------
# 2. 绘图
# ----------------------
plt.figure(figsize=(16, 10), dpi=100)

# 实际收敛误差（蓝色实线+圆点）
plt.loglog(n, error_actual, 'o-', color='#1f77b4', linewidth=2.5, markersize=7, label='实际收敛误差')

# 理论1阶收敛参考线（红色虚线）
plt.loglog(n_ref, error_ref, '--', color='#d62728', linewidth=2.5, label='理论1阶收敛参考线 (斜率=-1)')

# ----------------------
# 3. 图表美化
# ----------------------
plt.title('有限元离散收敛：误差收敛速率对比', fontsize=16, pad=15)
plt.xlabel('离散划分单元数量 n', fontsize=13, labelpad=10)
plt.ylabel('绝对误差 |π近似值 − π真值|', fontsize=13, labelpad=10)

# 网格（log坐标下显示主次网格）
plt.grid(True, which='both', linestyle='-', alpha=0.3)

# 图例
plt.legend(loc='upper right', fontsize=12)

# 调整布局
plt.tight_layout()

# 显示图片
plt.show()