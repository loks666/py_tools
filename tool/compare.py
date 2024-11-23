import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from scipy.optimize import minimize

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 房间参数设置（5m x 8m x 3m）
room_length = 8.0  # 房间长度 8 米
room_width = 5.0   # 房间宽度 5 米
room_height = 3.0  # 房间高度 3 米
room_volume = room_length * room_width * room_height  # 房间体积 120 m³

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
        width, height, depth = size  # 矩形净化器
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
alpha = 0.1  # 扩散系数
alpha *= room_volume / 120  # 根据房间体积调整（120m³是标准体积）

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
    for step in range(100):  # 进行100步迭代
        # 假设空气净化器能将其区域内的污染物浓度降低到零
        T_new[ac_mask] = 0.0

        # 其他区域的污染浓度扩散（模拟空气流动和污染物扩散）
        T_new[1:-1, 1:-1, 1:-1] = T[1:-1, 1:-1, 1:-1] * 0.9 + alpha * (
                T[1:-1, 1:-1, 2:] + T[1:-1, 1:-1, :-2] +
                T[1:-1, 2:, 1:-1] + T[1:-1, :-2, 1:-1] +
                T[2:, 1:-1, 1:-1] + T[:-2, 1:-1, 1:-1] -
                6 * T[1:-1, 1:-1, 1:-1])  # 三维扩散公式

        T = T_new.copy()

        # 在每步迭代时记录方差
        if step == 99:
            return T, np.var(T)  # 返回最终的净化结果和总方差

# 优化函数
def optimize_purifier(ac_shape):
    """
    优化净化器的尺寸，找到最佳尺寸。
    """
    # 定义目标函数
    def objective(size):
        pollution_concentration = np.random.uniform(0.5, 1.0, (nz, ny, nx))  # 初始污染浓度
        if ac_shape == 'rectangle':
            ac_size = (size[0], size[1], size[2])  # 矩形净化器尺寸
        elif ac_shape == 'circle':
            ac_size = size[0]  # 圆形净化器半径
        _, variance = simulate_purification(ac_shape, ac_size, pollution_concentration)
        return variance

    # 设置初始尺寸猜测值
    if ac_shape == 'rectangle':
        initial_guess = [1.0, 0.5, 1.5]  # 初始矩形净化器尺寸
        bounds = [(0.1, room_length), (0.1, room_width), (0.1, room_height)]  # 尺寸边界
    elif ac_shape == 'circle':
        initial_guess = [1.0]  # 初始圆形净化器半径
        bounds = [(0.1, min(room_length, room_width))]  # 半径边界

    # 优化
    result = minimize(objective, initial_guess, bounds=bounds, method='L-BFGS-B')
    return result.x, result.fun  # 返回最佳尺寸和对应的最小方差

# 可视化净化效果（选择合适的切片显示）
def plot_purification(T, title):
    plt.figure(figsize=(6, 5))
    plt.contourf(X[:, :, 0], Y[:, :, 0], T[nz//2, :, :], 20, cmap=cm.jet)  # 选择z轴中间的切片进行绘制
    plt.colorbar(label='污染浓度')
    plt.title(title)
    plt.xlabel('X 位置 (m)')
    plt.ylabel('Y 位置 (m)')
    plt.show()

# 主程序
def main():
    # 优化矩形净化器
    rect_best_size, rect_best_variance = optimize_purifier('rectangle')
    print(f"最佳矩形净化器尺寸: 长 = {rect_best_size[0]:.2f} m, 宽 = {rect_best_size[1]:.2f} m, 高 = {rect_best_size[2]:.2f} m")
    print(f"最佳矩形净化器的污染物浓度总方差: {rect_best_variance:.4f}")

    # 优化圆形净化器
    circle_best_size, circle_best_variance = optimize_purifier('circle')
    print(f"最佳圆形净化器半径: 半径 = {circle_best_size[0]:.2f} m")
    print(f"最佳圆形净化器的污染物浓度总方差: {circle_best_variance:.4f}")

    # 可视化最佳净化器效果
    pollution_concentration = np.random.uniform(0.5, 1.0, (nz, ny, nx))  # 初始污染浓度
    rect_T, _ = simulate_purification('rectangle', rect_best_size, pollution_concentration)
    plot_purification(rect_T, '最佳矩形净化器净化效果')
    # 修复传递单值半径
    circle_T, _ = simulate_purification('circle', circle_best_size[0], pollution_concentration)
    plot_purification(circle_T, '最佳圆形净化器净化效果')

    # 比较结果
    if rect_best_variance < circle_best_variance:
        print("矩形空气净化器在净化效果上更优。")
    elif rect_best_variance > circle_best_variance:
        print("圆形空气净化器在净化效果上更优。")
    else:
        print("矩形和圆形净化器的净化效果相同。")

# 运行主程序
if __name__ == "__main__":
    main()
