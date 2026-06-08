import numpy as np


def truss3d_element_stiffness(x1, x2, E, A):
    """
    计算三维杆单元的长度、方向余弦、6×6全局刚度矩阵
    x1, x2: [x, y, z] 节点坐标
    E: 弹性模量
    A: 截面积
    return: L, (cx, cy, cz), Ke(6×6)
    """
    x1 = np.array(x1, dtype=float)
    x2 = np.array(x2, dtype=float)

    dx = x2[0] - x1[0]
    dy = x2[1] - x1[1]
    dz = x2[2] - x1[2]

    L = np.sqrt(dx ** 2 + dy ** 2 + dz ** 2)

    # 退化单元检查
    if L < 1e-12:
        raise ValueError("错误：两个节点重合，无法计算杆单元！")

    cx = dx / L
    cy = dy / L
    cz = dz / L

    # 构造变换矩阵相关向量
    C = np.array([
        [cx ** 2, cx * cy, cx * cz],
        [cx * cy, cy ** 2, cy * cz],
        [cx * cz, cy * cz, cz ** 2]
    ])

    # 6×6刚度矩阵
    Ke = np.zeros((6, 6))
    factor = E * A / L

    Ke[0:3, 0:3] = factor * C
    Ke[0:3, 3:6] = -factor * C
    Ke[3:6, 0:3] = -factor * C
    Ke[3:6, 3:6] = factor * C

    return L, (cx, cy, cz), Ke


def truss3d_element_stress(x1, x2, E, A, de):
    """
    根据节点位移计算应变、应力、轴力
    de: [u1, v1, w1, u2, v2, w2]
    return: epsilon, sigma, N
    """
    x1 = np.array(x1, dtype=float)
    x2 = np.array(x2, dtype=float)
    de = np.array(de, dtype=float).reshape(6, 1)

    dx = x2[0] - x1[0]
    dy = x2[1] - x1[1]
    dz = x2[2] - x1[2]
    L = np.sqrt(dx ** 2 + dy ** 2 + dz ** 2)

    if L < 1e-12:
        raise ValueError("错误：节点重合！")

    cx = dx / L
    cy = dy / L
    cz = dz / L

    # 应变位移关系
    B = np.array([-cx, -cy, -cz, cx, cy, cz]).reshape(1, 6)
    epsilon = B @ de

    # 应力、轴力
    sigma = E * epsilon
    N = sigma * A

    # 修复：使用 .item() 提取标量，解决 TypeError
    return epsilon.item(), sigma.item(), N.item()


# ===================== 算例 1：沿x轴杆单元 =====================
print("=" * 60)
print("                   算例 1：沿x轴一维杆")
print("=" * 60)
x1 = [0, 0, 0]
x2 = [2, 0, 0]
E = 200e9
A = 1.0e-4
de = [0, 0, 0, 1e-3, 0, 0]

L1, dir1, Ke1 = truss3d_element_stiffness(x1, x2, E, A)
eps1, sig1, N1 = truss3d_element_stress(x1, x2, E, A, de)

print(f"单元长度 L = {L1:.2f} m")
print(f"方向余弦 cx,cy,cz = {dir1[0]:.1f}, {dir1[1]:.1f}, {dir1[2]:.1f}")
print(f"轴向应变 ε = {eps1:.6e}")
print(f"轴向应力 σ = {sig1 / 1e6:.2f} MPa")
print(f"轴力 N = {N1:.2e} N\n")

# ===================== 算例 2：空间任意方向杆 =====================
print("=" * 60)
print("                 算例 2：空间任意方向杆")
print("=" * 60)
x1 = [0, 0, 0]
x2 = [1, 2, 2]
E = 210e9
A = 2.0e-4
de = [0, 0, 0, 1e-3, 2e-3, 2e-3]

L2, dir2, Ke2 = truss3d_element_stiffness(x1, x2, E, A)
eps2, sig2, N2 = truss3d_element_stress(x1, x2, E, A, de)

print(f"单元长度 L = {L2:.1f} m")
print(f"方向余弦 cx,cy,cz = {dir2[0]:.3f}, {dir2[1]:.3f}, {dir2[2]:.3f}")
print(f"轴向应变 ε = {eps2:.6e}")
print(f"轴向应力 σ = {sig2 / 1e6:.2f} MPa")
print(f"轴力 N = {N2:.2e} N\n")

# ===================== 刚度矩阵性质验证 =====================
print("=" * 60)
print("              刚度矩阵性质验证（算例2）")
print("=" * 60)
print("Ke 对称？", np.allclose(Ke2, Ke2.T))
print("Ke 奇异？(行列式≈0)", abs(np.linalg.det(Ke2)) < 1e-6)
eig_val = np.linalg.eigvals(Ke2)
print("特征值非负？", np.all(eig_val.real >= -1e-6))