import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

# ���ṩ�ĳ�ʼ��������λ�õĴ���
num_agents = 221
radius = 5
agents_pos = [(np.cos(theta) * radius, np.sin(theta) * radius) for theta in np.linspace(0, 2 * np.pi, num_agents + 1)][
             1:]  # �ų�Բ��λ��


# �������ƺ���
def animate(frame, agents_pos, update_func):
    # ����������״̬
    agents_pos = update_func(agents_pos)
    ax.clear()
    ax.scatter(*agents_pos.T, color='red', s=25, zorder=3)
    ax.set_aspect('equal', adjustable='box')
    plt.draw()


# ѡ��MWMS-S��MWMS-J�㷨���ж���
def update_func_MWMS_S(agents_pos):
    # MWMS-S�㷨�ļ�ʾ������Ҫ��������ʵ�������߼���
    new_pos = agents_pos + 0.1 * (np.mean(agents_pos, axis=0) - agents_pos)
    return new_pos


def update_func_MWMS_J(agents_pos):
    # MWMS-J�㷨�ļ�ʾ������Ҫ��������ʵ�������߼���
    new_pos = agents_pos + 0.1 * (np.median(agents_pos, axis=0) - agents_pos)
    return new_pos


# ����ͼ�κ���
fig, ax = plt.subplots(figsize=(6, 6))

# ����MWMS-S�㷨�Ķ���
ani_S = FuncAnimation(fig, animate, fargs=(agents_pos, update_func_MWMS_S), frames=100, interval=200, blit=True)
ani_S.save('MWMS_S.gif', writer='pillow', fps=5)

# ����MWMS-J�㷨�Ķ���
ani_J = FuncAnimation(fig, animate, fargs=(agents_pos, update_func_MWMS_J), frames=100, interval=200, blit=True)
ani_J.save('MWMS_J.gif', writer='pillow', fps=5)

# ��ʾMWMS-S����
plt.show()
