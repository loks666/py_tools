import matplotlib.pyplot as plt
import numpy as np

# 载入文件
images_reconstructed = np.load('images_reconstructed.npy')

# 获取要显示的图像，例如获取第一张图
first_image = images_reconstructed[0]

# 使用matplotlib库进行显示
plt.figure(figsize=(5, 5))
plt.imshow(first_image, cmap='gray')  # 使用灰度色谱显示
plt.axis('off')
plt.show()
