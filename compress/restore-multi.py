import matplotlib.pyplot as plt
import numpy as np

images_reconstructed = np.load('images_reconstructed.npy')

# 设定行列数
num_rows = 10
num_cols = 10

# 计算要展示的图像总数
num_images = num_rows * num_cols

# 利用matplotlib进行展示
fig, axes = plt.subplots(num_rows, num_cols, figsize=(num_rows, num_cols))  # 创建一个 num_rows行num_cols列的子图
for i in range(num_rows):
    for j in range(num_cols):
        image = images_reconstructed[i * num_cols + j]
        axes[i, j].imshow(image, cmap='gray')  # 用灰度色谱显示
        axes[i, j].axis('off')

plt.tight_layout()  # 自动调整子图参数，使之填充整个图像区域
plt.show()
