import gzip

import numpy as np
from sklearn.decomposition import PCA


def read_idx_gz(filename):
    with gzip.open(filename, 'rb') as f:
        magic, num, rows, cols = np.frombuffer(f.read(16), '>i4,>i4,>i4,>i4', 1)[0]
        if magic == 2051:  # 图像文件
            return np.frombuffer(f.read(), dtype=np.uint8).reshape(num, rows, cols)
        elif magic == 2049:  # 标签文件
            return np.frombuffer(f.read(), dtype=np.uint8)
        else:
            raise ValueError(f'Unknown file type: {filename}')


# 读取raw文件夹下的平衡数据集
images = read_idx_gz('./raw/emnist-balanced-train-images-idx3-ubyte.gz')
labels = read_idx_gz('./raw/emnist-balanced-train-labels-idx1-ubyte.gz')

# 随机选择1000个样本，如果读取失败则继续尝试
images_sample = []
labels_sample = []
count = 0
while count < 1000:
    try:
        index = np.random.randint(images.shape[0])
        images_sample.append(images[index])
        labels_sample.append(labels[index])
        count += 1
    except Exception as e:
        print(f"Failed to read image {index}: {e}")

images_sample = np.array(images_sample)
labels_sample = np.array(labels_sample)

# 将图像数据转换为一维
images_1d = images_sample.reshape(-1, 28 * 28)

# 创建PCA对象，目标维度为50
pca = PCA(n_components=50)

# 对图像数据进行PCA降维
images_pca = pca.fit_transform(images_1d)

# 使用PCA对象的inverse_transform方法从压缩表示中进行重建
images_reconstructed = pca.inverse_transform(images_pca)

# 将重建的图像数据转换回原始的二维形状
images_reconstructed = images_reconstructed.reshape(-1, 28, 28)

# 保存重建的图像数据
np.save('images_reconstructed.npy', images_reconstructed)
