import socket

import matplotlib.pyplot as plt
import numpy as np

# 初始化20个通道的绘图
fig, axs = plt.subplots(20, 1, figsize=(10, 20))
lines = []
for ax in axs:
    line, = ax.plot([], [], lw=2)
    lines.append(line)

plt.ion()
plt.show()

data_storage = []


# 接收TCP数据
def receive_tcp_data(ip, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip, port))
        while True:
            data = s.recv(1024)
            if not data:
                break
            yield data


# 解析接收到的数据
def parse_data(data):
    parsed_data = []
    for i in range(0, len(data), 20):
        channel_data = data[i:i + 20]
        if len(channel_data) == 20:
            # 将字节数据转换为数值
            channel_data_values = [int.from_bytes(channel_data[j:j + 2], byteorder='big') for j in
                                   range(0, len(channel_data), 2)]
            parsed_data.append(channel_data_values)
    return parsed_data


# 更新绘图
def update_plot(channel_data):
    for i, line in enumerate(lines):
        line.set_ydata(channel_data[i])
        line.set_xdata(np.arange(len(channel_data[i])))
        axs[i].relim()
        axs[i].autoscale_view()
    plt.draw()
    plt.pause(0.001)


# 保存数据
def save_data(data, filename='recive.txt'):
    with open(filename, 'a') as f:
        for line in data:
            f.write(' '.join(format(x, '02X') for x in line) + '\n')


# 从文件读取数据
def read_data_from_file(filepath):
    with open(filepath, 'r') as f:
        data = []
        for line in f:
            bytes_line = bytes.fromhex(line.strip().replace(' ', ''))
            data.append(bytes_line)
    return data


# 从TCP接收数据的处理流程
def process_tcp_data(ip, port):
    while True:
        for data in receive_tcp_data(ip, port):
            parsed_data = parse_data(data)
            update_plot(parsed_data)
            save_data(parsed_data)


# 从文件读取数据的处理流程
def process_file_data(filepath):
    file_data = read_data_from_file(filepath)
    for data in file_data:
        parsed_data = parse_data(data)
        update_plot(parsed_data)
        save_data(parsed_data)


if __name__ == '__main__':
    ip = '192.168.4.1'
    port = 4321
    filepath = 'data.txt'

    # 使用其中一个方法，注释掉另一个
    # 处理TCP数据
    # process_tcp_data(ip, port)

    # 处理文件数据
    process_file_data(filepath)
