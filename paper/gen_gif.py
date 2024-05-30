import imageio
import networkx as nx
import numpy as np
from matplotlib import pyplot as plt

# 您提供的初始化智能体位置的代码
num_agents = 221
radius = 5
agents_pos = [(np.cos(theta) * radius, np.sin(theta) * radius) for theta in np.linspace(0, 2 * np.pi, num_agents + 1)][
             1:]  # 排除圆心位置


# Motif-Aware Weighted Multi-agent System (MWMS) 方法
def mwms(G, alpha, epsilon, iterations):
    n = len(G.nodes)
    states = np.random.rand(n)
    all_states = [states.copy()]

    motif_matrix = calculate_motif_matrix(G)
    for _ in range(iterations):
        new_states = states.copy()
        for i in range(n):
            neighbors = list(G.neighbors(i))
            if len(neighbors) > 0:
                weighted_sum = sum(
                    (motif_matrix[i, j] / (np.sum(motif_matrix[i, neighbors]) + 1e-10) if j in neighbors else 0) *
                    states[j] for j in range(n))
                new_states[i] = states[i] + epsilon * (weighted_sum - states[i])
        states = new_states
        all_states.append(states.copy())

    return all_states


def calculate_motif_matrix(G):
    motif_matrix = np.zeros((len(G.nodes), len(G.nodes)))  # Placeholder for the motif matrix
    # 这里需要根据实际的网络拓扑计算motif矩阵，下面只是示例代码
    for i in range(len(G.nodes)):
        for j in range(i + 1, len(G.nodes)):
            if nx.has_path(G, i, j, path_length=2):  # 检查是否有长度为2的路径，即是否有triangle motif
                motif_matrix[i, j] += 1
                motif_matrix[j, i] += 1
    return motif_matrix


# 创建图形和轴
fig, ax = plt.subplots(figsize=(6, 6))


# 生成MWMS算法的动画
def create_gif(all_states, G, filename, title='MWMS Convergence'):
    images = []
    for iteration, states in enumerate(all_states):
        plt.figure(figsize=(6, 6))
        # 根据states绘制节点位置
        node_colors = states
        nx.draw(G, pos={node: G.nodes[node]['pos'] for node in G.nodes}, node_color=node_colors, with_labels=True,
                node_size=50)
        plt.title(title + f' Iteration {iteration}')
        plt.savefig('temp.png')
        plt.close()
        images.append(imageio.imread('temp.png'))
    imageio.mimsave(filename, images, duration=0.1)


# 创建网络拓扑
G = nx.Graph()
for i, pos in enumerate(agents_pos):
    G.add_node(i, pos=pos)

# 添加边，这里简化处理，根据节点位置计算是否相邻
for i in range(num_agents):
    for j in range(i + 1, num_agents):
        if np.linalg.norm(np.array(agents_pos[i]) - np.array(agents_pos[j])) <= 1:
            G.add_edge(i, j)

# 计算Motif矩阵
G.motif_matrix = calculate_motif_matrix(G)

# 参数
alpha = 0.5
epsilon = 0.1
iterations = 100

# 运行MWMS算法并生成动画
states_s = mwms(G, alpha, epsilon, iterations)
create_gif(states_s, G, 'MWMS_S.gif', title='MWMS-S')

states_j = mwms(G, alpha, epsilon, iterations)
create_gif(states_j, G, 'MWMS_J.gif', title='MWMS-J')
