import os
import random
import numpy as np
from PIL import Image

def softmax(x):
    """计算 Softmax 概率"""
    exp_x = np.exp(x - np.max(x))  # 避免数值溢出
    return exp_x / exp_x.sum()

def calculate_energy(turns, path_length):
    """计算路径的能量函数 E = N_turn / L_path^2"""
    if path_length == 0:
        return float('inf')  # 避免除零错误
    return turns / (path_length ** 2)

def generate_hamiltonian_path(rows, cols, debug=False):
    """基于论文实现 Hamiltonian Path 生成路径"""
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # 右、下、左、上
    visited = np.zeros((rows, cols), dtype=int)
    start = (0, 0)
    end = (rows - 1, cols - 1)
    path_stack = [(start[0], start[1], None, 0, 0)]  # (x, y, prev_dir, turns, path_length)
    visited[start] = 1

    while path_stack:
        x, y, prev_dir, turns, path_length = path_stack[-1]

        if (x, y) == end and np.sum(visited) > rows * cols * 0.6:
            print(f"✅ 找到合理路径！")
            visited = enforce_ribs(visited, min_ribs=2)  # ✅ 强制增加肋条
            return visited

        neighbors = [(dx, dy) for dx, dy in directions if 0 <= x + dx < rows and 0 <= y + dy < cols and visited[x + dx, y + dy] == 0]

        if not neighbors:
            while path_stack:
                last_x, last_y, _, _, _ = path_stack.pop()
                visited[last_x, last_y] = 0
                new_neighbors = [(dx, dy) for dx, dy in directions if 0 <= last_x + dx < rows and 0 <= last_y + dy < cols and visited[last_x + dx, last_y + dy] == 0]
                if len(new_neighbors) > 1:
                    break
            continue

        probs = softmax(-np.array([calculate_energy(turns + (1 if prev_dir and (dx, dy) != prev_dir else 0), path_length + 1) for dx, dy in neighbors]) * random.uniform(0.8, 1.2))
        chosen_idx = np.random.choice(len(neighbors), p=probs)
        dx, dy = neighbors[chosen_idx]

        visited[x + dx, y + dy] = 1
        path_stack.append((x + dx, y + dy, (dx, dy), turns + (1 if (dx, dy) != prev_dir else 0), path_length + 1))

    print("❌ 未能生成完整路径，返回 None")
    return None



def enforce_ribs(matrix, min_ribs=2):
    """确保路径矩阵中有空白区域（肋条），避免全黑图像"""
    rows, cols = matrix.shape
    zero_positions = list(zip(*np.where(matrix == 0)))

    # 只有少量空白（肋条）时，手动清除一些路径点
    if len(zero_positions) < min_ribs:
        ones_positions = list(zip(*np.where(matrix == 1)))
        random.shuffle(ones_positions)

        for pos in ones_positions:
            matrix[pos] = 0  # 清除路径
            zero_positions.append(pos)
            if len(zero_positions) >= min_ribs:
                break  # 确保至少有 min_ribs 个肋条

    return matrix

def save_matrix_as_image(matrix, filename, cell_size=10, debug=False):
    """将路径矩阵保存为 PNG 图像，并添加日志"""
    rows, cols = matrix.shape
    img = Image.new("RGB", (cols * cell_size, rows * cell_size), color="white")  # 创建白色背景的图像
    pixels = img.load()  # 获取像素操作句柄

    print("\n🎨 开始绘制图像...")
    for i in range(rows):
        for j in range(cols):
            if matrix[i, j] == 1:  # 黑色表示路径
                if debug:
                    print(f"🖌️ 绘制路径点: ({i}, {j}) -> 黑色区域")
                for di in range(cell_size):
                    for dj in range(cell_size):
                        pixels[j * cell_size + dj, i * cell_size + di] = (0, 0, 0)  # 黑色路径填充

    img.save(filename)
    print(f"✅ 路径图像已保存为 {filename}")


# 运行测试
if __name__ == "__main__":
    print("🚀 开始 3×3 网格的路径生成测试...")
    result = generate_hamiltonian_path(3, 3, debug=True)

    if result is not None:
        print("\n📝 确保路径矩阵正确：")
        print(result)  # 打印路径矩阵，检查是否符合预期

        save_matrix_as_image(result, "path_3x3.png", debug=True)
        print("🎉 成功生成 3×3 路径，并已保存为 path_3x3.png")
    else:
        print("❌ 失败，无法找到路径")
