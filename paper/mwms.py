import imageio
import networkx as nx
import numpy as np
from matplotlib import pyplot as plt


def mwms_s(G, alpha, epsilon, iterations):
    n = len(G.nodes)
    states = np.random.rand(n)
    all_states = [states.copy()]

    if not hasattr(G, 'motif_matrix'):
        G.motif_matrix = calculate_motif_matrix(G)

    for _ in range(iterations):
        new_states = states.copy()
        for i in range(n):  # Use integer indices
            neighbors = list(G.neighbors(i))
            if len(neighbors) > 0:
                weighted_sum = sum(G.motif_matrix[i, j] / (np.sum(G.motif_matrix[i, neighbors]) + 1e-10) * states[j] for j in neighbors)
                new_states[i] = states[i] + epsilon * (weighted_sum - states[i])
        states = new_states
        all_states.append(states.copy())

    return all_states


def calculate_motif_matrix(G):
    motif_matrix = np.zeros((len(G.nodes), len(G.nodes)))  # Placeholder for the motif matrix
    return motif_matrix


def mwms_j(G, alpha, epsilon, iterations):
    n = len(G.nodes)
    states = np.random.rand(n)
    all_states = [states.copy()]

    for _ in range(iterations):
        new_states = np.zeros(n)
        for i in range(n):  # Use integer indices
            neighbors = list(G.neighbors(i))
            if len(neighbors) > 0:
                weighted_sum = sum((G.motif_matrix[i, j] + 1) / (np.sum(G.motif_matrix[i, neighbors]) + 1) * (states[j] if j != i else states[i]) for j in neighbors)
                new_states[i] = weighted_sum / (np.sum(G.motif_matrix[i, neighbors]) + 1)
        states = new_states
        all_states.append(states.copy())

    return all_states


def top_7():
    G = nx.Graph()
    um_agents = 221
    radius = 5
    layers = int(radius / 0.5)
    agents_per_layer = 4
    node_id = 0  # Add a unique integer identifier for each node

    for layer in range(layers):
        r = 0.5 + 0.5 * layer
        num_agents_in_layer = agents_per_layer * (layer + 1)
        for i in range(num_agents_in_layer):
            theta = 2 * np.pi / num_agents_in_layer * i
            x = r * np.cos(theta)
            y = r * np.sin(theta)
            G.add_node(node_id, pos=(x, y))  # Store the position as a node attribute
            node_id += 1

    for i in range(node_id):
        for j in range(i + 1, node_id):
            if np.linalg.norm(np.array(G.nodes[i]['pos']) - np.array(G.nodes[j]['pos'])) <= 1:
                G.add_edge(i, j)

    return G


def create_gif(all_states, G, filename):
    images = []
    for states in all_states:
        plt.figure(figsize=(6, 6))
        nx.draw(G, pos={node: G.nodes[node]['pos'] for node in range(len(G.nodes))}, node_color='red', with_labels=True, node_size=50)
        plt.title('Iteration')
        plt.savefig('temp.png')
        plt.close()
        images.append(imageio.imread('temp.png'))
    imageio.mimsave(filename, images, duration=0.1)


if __name__ == '__main__':
    G = top_7()
    alpha = 0.5
    epsilon = 0.1
    iterations = 100
    states_s = mwms_s(G, alpha, epsilon, iterations)
    states_j = mwms_j(G, alpha, epsilon, iterations)
    create_gif(states_s, G, 'mwms_s.gif')
    create_gif(states_j, G, 'mwms_j.gif')
