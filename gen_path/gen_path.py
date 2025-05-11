import os
import math
import random
import time
import argparse
from PIL import Image
import numpy as np

# 参数解析器
parser = argparse.ArgumentParser(description="生成流场路径图像")
parser.add_argument('--max-images', type=int, default=13000, help='要生成的最大图像数量')
args = parser.parse_args()

output_dir = "img"
os.makedirs(output_dir, exist_ok=True)

# 网格和分辨率设置
n1, n2 = 9, 9
delta = 14  # 每个单元格大小设置为14像素，生成128x128图像

# 能量函数
def compute_energy(num_turns, path_length):
    return num_turns / (path_length ** 2)

# 初始化路径
def initialize_path(n1, n2):
    path = []
    visited = [[False] * n2 for _ in range(n1)]
    for c in range(n2):
        path.append((0, c))
        visited[0][c] = True
    for r in range(1, n1):
        path.append((r, n2 - 1))
        visited[r][n2 - 1] = True
    num_turns = 1
    return path, visited, num_turns

# 生成候选路径
def generate_candidates(path, visited, num_turns):
    candidates = []
    weights = []
    edges_count = len(path) - 1
    for k in range(len(path) - 1):
        rA, cA = path[k]
        rB, cB = path[k + 1]
        directions = []
        if rA == rB:
            directions = [(-1, 0), (1, 0)]
        elif cA == cB:
            directions = [(0, -1), (0, 1)]
        for dr, dc in directions:
            X, Y = (rA + dr, cA + dc), (rB + dr, cB + dc)
            if (0 <= X[0] < n1 and 0 <= X[1] < n2 and
                0 <= Y[0] < n1 and 0 <= Y[1] < n2 and
                not visited[X[0]][X[1]] and not visited[Y[0]][Y[1]]):
                new_num_turns = num_turns + 2
                E = compute_energy(new_num_turns, edges_count + 2)
                weight = math.exp(-E)
                candidates.append((k, X, Y, new_num_turns))
                weights.append(weight)
    if not candidates:
        return None, None, None
    pick = random.choices(candidates, weights=weights)[0]
    return pick[0], (pick[1], pick[2]), pick[3]

# 路径转图像
def path_to_image(path):
    img = np.zeros((n1 * delta + 2, n2 * delta + 2), dtype=np.uint8)
    border = 1
    cell_interior = delta - 1
    half = cell_interior // 2
    channel_width = delta // 2  # 白色通道宽度占单元格的一半
    for (r, c) in path:
        center_r = border + r * delta + half
        center_c = border + c * delta + half
        img[center_r - channel_width//2:center_r + channel_width//2 + 1,
            center_c - channel_width//2:center_c + channel_width//2 + 1] = 1
    for i in range(len(path) - 1):
        r1, c1 = path[i]
        r2, c2 = path[i + 1]
        cr1 = border + r1 * delta + half
        cc1 = border + c1 * delta + half
        cr2 = border + r2 * delta + half
        cc2 = border + c2 * delta + half
        if r1 == r2:
            img[cr1 - channel_width//2:cr1 + channel_width//2 + 1,
                min(cc1, cc2):max(cc1, cc2) + 1] = 1
        elif c1 == c2:
            img[min(cr1, cr2):max(cr1, cr2) + 1,
                cc1 - channel_width//2:cc1 + channel_width//2 + 1] = 1
    return img

# 主程序
success_count = 0
attempt_count = 0
start_time = time.time()

while success_count < args.max_images:
    attempt_count += 1
    path, visited_matrix, num_turns = initialize_path(n1, n2)
    iter_count = 0
    visited_count = len(path)
    while visited_count < n1 * n2 and iter_count < n1 * n2 * 10:
        iter_count += 1
        result = generate_candidates(path, visited_matrix, num_turns)
        if result[0] is None:
            break
        edge_index, (X, Y), num_turns = result
        path.insert(edge_index + 1, X)
        path.insert(edge_index + 2, Y)
        visited_matrix[X[0]][X[1]] = True
        visited_matrix[Y[0]][Y[1]] = True
        visited_count += 2
    if visited_count == n1 * n2:
        img_array = path_to_image(path)
        img = Image.fromarray((img_array * 255).astype('uint8'))
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"spiral_{n1}x{n2}_{success_count:06d}_{timestamp}.png"
        img.save(os.path.join(output_dir, filename))
        success_count += 1
        elapsed = time.time() - start_time
        print(f"[{success_count}/{args.max_images}] 已生成: {filename}，尝试次数: {attempt_count}，耗时: {elapsed:.2f}s")

print("图像生成任务完成！")