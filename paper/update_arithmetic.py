import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

# 您提供的初始化智能体位置的代码
num_agents = 221
radius = 5
agents_pos = [(np.cos(theta) * radius, np.sin(theta) * radius) for theta in np.linspace(0, 2 * np.pi, num_agents + 1)][
             1:]  # 排除圆心位置


# 动画绘制函数
def animate(frame, agents_pos, update_func):
    # 更新智能体状态
    agents_pos = update_func(agents_pos)
    ax.clear()
    ax.scatter(*agents_pos.T, color='red', s=25, zorder=3)
    ax.set_aspect('equal', adjustable='box')
    plt.draw()


# 选择MWMS-S或MWMS-J算法进行动画
def update_func_MWMS_S(agents_pos):
    # MWMS-S算法的简化示例（需要根据论文实现完整逻辑）
    new_pos = agents_pos + 0.1 * (np.mean(agents_pos, axis=0) - agents_pos)
    return new_pos


def update_func_MWMS_J(agents_pos):
    # MWMS-J算法的简化示例（需要根据论文实现完整逻辑）
    new_pos = agents_pos + 0.1 * (np.median(agents_pos, axis=0) - agents_pos)
    return new_pos


# 创建图形和轴
fig, ax = plt.subplots(figsize=(6, 6))

# 生成MWMS-S算法的动画
ani_S = FuncAnimation(fig, animate, fargs=(agents_pos, update_func_MWMS_S), frames=100, interval=200, blit=True)
ani_S.save('MWMS_S.gif', writer='pillow', fps=5)

# 生成MWMS-J算法的动画
ani_J = FuncAnimation(fig, animate, fargs=(agents_pos, update_func_MWMS_J), frames=100, interval=200, blit=True)
ani_J.save('MWMS_J.gif', writer='pillow', fps=5)

# 显示MWMS-S动画
plt.show()
