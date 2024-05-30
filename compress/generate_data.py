import gzip
import os

import numpy as np
from PIL import Image


def read_idx(filename):
    with gzip.open(filename, 'rb') as f:
        zero, zero, data_type, dims = np.frombuffer(f.read(4), dtype=np.uint8)
        shape = tuple(np.frombuffer(f.read(dims * 4), dtype='>i4'))
        return np.frombuffer(f.read(), dtype=np.uint8).reshape(shape)


# 列出所有的子集
# subsets = ['balanced', 'byclass', 'bymerge', 'digits', 'letters', 'mnist']
subsets = ['balanced']

for subset in subsets:
    # 读取图像数据
    images = read_idx(f'raw\\emnist-{subset}-train-images-idx3-ubyte.gz')

    # 创建保存图像的文件夹，如果不存在
    if not os.path.exists(f'imgs\\{subset}'):
        os.makedirs(f'imgs\\{subset}')

    # 将每个图像保存为JPG格式
    for i in range(1001):
        img = Image.fromarray(images[i])
        img = img.convert("L")
        img.save(f'imgs\\{subset}\\{i}.jpg')
