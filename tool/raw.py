import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from scipy.optimize import minimize

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 1. 房间参数设置（依据题目给定尺寸）
room_length = 8.0  # 房间长度 8 米
room_width = 5.0   # 房间宽度 5 米
room_height = 3.0  # 房间高度 3 米（根据题目修改）

# 网格划分
nx = 50  # x方向网格数
ny = 50  # y方向网格数
nz = 30  # z方向网格数（新增）
dx = room_length / (nx - 1)  # 网格间距（x方向）
dy = room_width / (ny - 1)  # 网格间距（y方向）
dz = room_height / (nz - 1)  # 网格间距（z方向）
x = np.linspace(0, room_length, nx)  # x坐标
y = np.linspace(0, room_width, ny)  # y坐标
z = np.linspace(0, room_height, nz)  # z坐标
X, Y, Z = np.meshgrid(x, y, z)

# 空气净化器的不同形状和尺寸
def get_ac_mask(shape, size, position):
    """
    根据空气净化器的形状、尺寸和位置，生成净化区域的掩膜。
    """
    mask = np.zeros((nz, ny, nx), dtype=bool)
    if shape == 'rectangle':
        width, height, depth = size  # 新增深度（对于矩形空调）
        x_start = int(position[0] / dx)
        y_start = int(position[1] / dy)
        z_start = int(position[2] / dz)
        x_end = int((position[0] + width) / dx)
        y_end = int((position[1] + height) / dy)
        z_end = int((position[2] + depth) / dz)
        mask[z_start:z_end, y_start:y_end, x_start:x_end] = True
    elif shape == 'circle':
        radius = size
        cx = int(position[0] / dx)
        cy = int(position[1] / dy)
        cz = int(position[2] / dz)
        for i in range(nz):
            for j in range(ny):
                for k in range(nx):
                    if (i - cz) ** 2 + (j - cy) ** 2 + (k - cx) ** 2 <= (radius / dx) ** 2:
                        mask[i, j, k] = True
    return mask

# 空气流动和污染物扩散系数
alpha = 0.1

# 模拟空气净化效果
def simulate_purification(ac_shape, ac_size, pollution_concentration):
    """
    模拟空气净化器在不同形状和尺寸下的净化效果。
    """
    T = np.copy(pollution_concentration)  # 初始污染浓度场
    T_new = T.copy()  # 临时变量用于更新浓度场

    # 获取空气净化器区域的掩膜
    ac_mask = get_ac_mask(ac_shape, ac_size, position=(room_length / 2, room_width / 2, room_height / 2))

    # 模拟净化过程
    for _ in range(100):  # 进行100步迭代
        # 假设空气净化器能将其区域内的污染物浓度降低到零
        T_new[ac_mask] = 0.0

        # 其他区域的污染浓度扩散（模拟空气流动和污染物扩散）
        T_new[1:-1, 1:-1, 1:-1] = T[1:-1, 1:-1, 1:-1] * 0.9 + alpha * (
                T[1:-1, 1:-1, 2:] + T[1:-1, 1:-1, :-2] +
                T[1:-1, 2:, 1:-1] + T[1:-1, :-2, 1:-1] +
                T[2:, 1:-1, 1:-1] + T[:-2, 1:-1, 1:-1] -
                6 * T[1:-1, 1:-1, 1:-1])  # 三维扩散公式

        T = T_new.copy()

    return T

# 2. 定义目标函数：最小化净化后的污染物浓度的总方差
def objective(params):
    ac_shape = 'rectangle'  # 固定形状为矩形
    ac_size = (params[2], params[1], params[2])  # 空气净化器尺寸（长，宽，高）
    pollution_concentration = np.random.uniform(0.5, 1.0, (nz, ny, nx))  # 初始污染浓度（随机生成）

    # 模拟净化效果
    T = simulate_purification(ac_shape, ac_size, pollution_concentration)

    # 计算净化后的污染物浓度总方差
    return np.var(T)

# 初始猜测：空气净化器尺寸（长、宽、高）
initial_guess = [1.0, 0.5, 1.5]  # 空气净化器的初始尺寸：长1.0米、宽0.5米、高1.5米

# 设置约束条件（空气净化器的尺寸不能超出房间尺寸）
bounds = [(0.1, room_length), (0.1, room_width), (0.1, room_height)]  # 尺寸范围（最小0.1米，最大房间尺寸）

# 3. 执行优化
result = minimize(objective, initial_guess, bounds=bounds, method='L-BFGS-B')

# 输出最佳结果
best_ac_size = result.x
print(f"最佳空气净化器尺寸: 长 = {best_ac_size[0]:.2f} 米, 宽 = {best_ac_size[1]:.2f} 米, 高 = {best_ac_size[2]:.2f} 米")

# 4. 计算最佳尺寸下的净化效果
best_purification = simulate_purification('rectangle', (best_ac_size[0], best_ac_size[1], best_ac_size[2]), np.random.uniform(0.5, 1.0, (nz, ny, nx)))

# 可视化净化效果（选择合适的切片显示）
def plot_purification(T, title):
    plt.figure(figsize=(6, 5))
    plt.contourf(X[:, :, 0], Y[:, :, 0], T[nz//2, :, :], 20, cmap=cm.jet)  # 选择z轴中间的切片进行绘制
    plt.colorbar(label='污染浓度')
    plt.title(title)
    plt.xlabel('X 位置 (m)')
    plt.ylabel('Y 位置 (m)')
    plt.show()

# 5. 可视化最佳设计下的净化效果
plot_purification(best_purification, '最佳空气净化器设计的净化效果')
