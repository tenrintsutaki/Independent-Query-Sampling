import numpy as np


def rotate_vector(vector, deg_x, deg_y, deg_z):
    """
    将三维向量绕 x, y, z 轴旋转指定角度。

    参数:
        vector (np.array): 三维向量，形状为 (3,)
        deg_x (float): 绕 x 轴旋转的角度（度）
        deg_y (float): 绕 y 轴旋转的角度（度）
        deg_z (float): 绕 z 轴旋转的角度（度）

    返回:
        np.array: 旋转后的三维向量
    """
    # 将角度转换为弧度
    theta_x = np.radians(deg_x)
    theta_y = np.radians(deg_y)
    theta_z = np.radians(deg_z)

    # 绕 x 轴旋转矩阵
    Rx = np.array([
        [1, 0, 0],
        [0, np.cos(theta_x), -np.sin(theta_x)],
        [0, np.sin(theta_x), np.cos(theta_x)]
    ])

    # 绕 y 轴旋转矩阵
    Ry = np.array([
        [np.cos(theta_y), 0, np.sin(theta_y)],
        [0, 1, 0],
        [-np.sin(theta_y), 0, np.cos(theta_y)]
    ])

    # 绕 z 轴旋转矩阵
    Rz = np.array([
        [np.cos(theta_z), -np.sin(theta_z), 0],
        [np.sin(theta_z), np.cos(theta_z), 0],
        [0, 0, 1]
    ])

    # 组合旋转：先绕 z 轴，再绕 y 轴，最后绕 x 轴
    rotated_vector = Rz @ Ry @ Rx @ vector
    return rotated_vector


# 示例
vector = np.array([-3.4, -1.5, -3])  # 初始向量
deg_x = 2  # 绕 x 轴旋转 45 度
deg_y = -7  # 绕 y 轴旋转 30 度
deg_z = 5  # 绕 z 轴旋转 60 度

result = rotate_vector(vector, deg_x, deg_y, deg_z)
print("旋转后的向量:", result)
result = result + np.array([4.5, 3.5, 6])
print("旋转后的向量:", result)