import warnings
warnings.filterwarnings("ignore")

import math
import matplotlib.pyplot as plt
from matplotlib.ticker import LogLocator, FuncFormatter

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

def compute_pi(n):
    theta = 2 * math.pi / n
    side_length = 2 * math.sin(theta / 2)
    perimeter = n * side_length
    return perimeter / 2

n_list = [4, 8, 16, 32, 64, 128, 256, 512, 1024]
pi_true = math.pi
pi_approx = [compute_pi(n) for n in n_list]
error_actual = [abs(p - pi_true) for p in pi_approx]

# --- 计算收敛阶 ---
p_list = []
for i in range(1, len(n_list)):
    n1, n2 = n_list[i-1], n_list[i]
    e1, e2 = error_actual[i-1], error_actual[i]
    p = math.log(e1 / e2) / math.log(n2 / n1)  # 收敛阶 p
    p_list.append(p)

avg_p = sum(p_list) / len(p_list)  # 平均收敛阶

# --- 绘制参考线（二阶收敛）---
error_ref = [(math.pi**3)/6 / (n**2) for n in n_list]

plt.figure(figsize=(10,6), dpi=120)

plt.plot(n_list, error_actual, 'o-', color='#1f77b4',
         linewidth=2, markersize=5, label='实际收敛误差')

plt.plot(n_list, error_ref, '--', color='#d62728',
         linewidth=2, label=f'理论2阶收敛参考线(斜率=-2)')

plt.xscale('log', base=10)
plt.yscale('log', base=10)
ax = plt.gca()

def log_formatter(x, pos):
    exp = int(round(math.log10(x)))
    return r'$10^{%d}$' % exp

ax.xaxis.set_major_locator(LogLocator(base=10, subs=(1.0,)))
ax.yaxis.set_major_locator(LogLocator(base=10, subs=(1.0,)))
ax.xaxis.set_major_formatter(FuncFormatter(log_formatter))
ax.yaxis.set_major_formatter(FuncFormatter(log_formatter))

plt.xlabel('离散划分单元数量 n')
plt.ylabel('绝对误差 |π近似值 - π真值|')
plt.title(f'有限元离散收敛：误差收敛速率对比\n实际平均收敛阶 p ≈ {avg_p:.2f}')

plt.grid(True, which='both', alpha=0.3, linestyle='-')
plt.legend()
plt.tight_layout()

plt.show()

# --- 打印收敛阶信息 ---
print("各段收敛阶：")
for i, p in enumerate(p_list, 1):
    print(f"n={n_list[i-1]} → n={n_list[i]}: p = {p:.4f}")
print(f"\n平均收敛阶：p_avg = {avg_p:.4f}")