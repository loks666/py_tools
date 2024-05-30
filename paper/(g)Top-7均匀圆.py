import matplotlib.pyplot as plt
import numpy as np

num_agents = 221
radius = 5

agents_pos = []  # 用于存储智能体位置
agents_pos.append((0, 0))
layers = int(radius / 0.5)  # 计算层数
agents_per_layer = 4  # 每层比上一层多4个智能体

for layer in range(layers):
    r = 0.5 + 0.5 * layer  # 计算当前层到圆心的距离,每层递增0.5
    num_agents_in_layer = agents_per_layer * (layer + 1)  # 计算当前层的智能体数量
    for i in range(num_agents_in_layer):
        theta = 2 * np.pi / num_agents_in_layer * i
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        agents_pos.append((x, y))


def add_edges(pos):  # 加连接线
    edges = []
    for i in range(len(pos)):
        for j in range(i + 1, len(pos)):
            dist = np.linalg.norm(pos[i] - pos[j])
            if dist <= 1:
                edges.append((pos[i], pos[j]))
    return edges


agents_pos = np.array(agents_pos)
neighbour_edges = add_edges(agents_pos)

# 可视化
plt.figure(figsize=(6, 6))
plt.scatter(agents_pos[:1, 0], agents_pos[:1, 1], color='red', s=25, zorder=3)  # 圆心位置
plt.scatter(agents_pos[1:, 0], agents_pos[1:, 1], color='red', s=25, zorder=3)  # 其他位置
plt.gca().set_aspect('equal', adjustable='box')
for edge in neighbour_edges:
    plt.plot([edge[0][0], edge[1][0]], [edge[0][1], edge[1][1]], linestyle='-.', linewidth=0.3, c='k')
plt.xlim(-5, 5)
plt.ylim(-5, 5)
plt.xticks([-5, 0, 5])
plt.yticks([-5, 0, 5])
plt.show()

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from sklearn.cluster import KMeans


# K-means算法
def kmeans_clustering(pos, n_clusters, max_iter):
    kmeans = KMeans(n_clusters=n_clusters, init='random', max_iter=1, n_init=1)
    kmeans.fit(pos)
    for _ in range(max_iter - 1):
        kmeans = KMeans(n_clusters=n_clusters, init=kmeans.cluster_centers_, max_iter=1, n_init=1)
        kmeans.fit(pos)
    return kmeans.labels_, kmeans.cluster_centers_


# 参数
n_clusters = 5  # 假设我们想要将智能体划分为5个群体
iterations = 10  # K-means算法的迭代次数

# 创建图形
fig, ax = plt.subplots()

# 初始化散点图和群体中心
scatter = ax.scatter(agents_pos[:, 0], agents_pos[:, 1], c=np.zeros_like(agents_pos[:, 0]), s=25, zorder=3)
centers_scatter = ax.scatter([], [], c='black', s=100, marker='x', zorder=4)


# 更新函数
def update(i):
    labels, centers = kmeans_clustering(agents_pos, n_clusters, i + 1)
    scatter.set_array(labels)
    centers_scatter.set_offsets(centers)


# 创建动画
ani = FuncAnimation(fig, update, frames=iterations, interval=200)
ani.save('kmeans.gif', writer='imagemagick')

# 显示动画
plt.show()
