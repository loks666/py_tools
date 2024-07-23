import matplotlib.pyplot as plt

# 从文件读取数据
def read_data_from_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        if len(lines) > 1:
            data_hex = lines[1].strip().replace(' ', '')
            data_bytes = bytes.fromhex(data_hex)
            return data_bytes
        else:
            raise ValueError("文件中没有第二行数据")

# 解析数据
def parse_data(data):
    channel = int.from_bytes(data[0:2], byteorder='big')
    data_points = list(data[2:-1])  # 跳过前两个字节和最后一个字节
    return channel, data_points

# 绘制数据
def plot_data(channel, data_points):
    plt.figure(figsize=(10, 5))
    plt.plot(data_points, label=f'Channel {channel}')
    plt.xlabel('Sample Index')
    plt.ylabel('Sample Value')
    plt.title(f'Ultrasound Data Channel {channel}')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == '__main__':
    filepath = 'data.txt'  # 替换为你的数据文件路径
    try:
        data = read_data_from_file(filepath)
        channel, data_points = parse_data(data)
        plot_data(channel, data_points)
    except ValueError as e:
        print(e)
    except UnicodeDecodeError as e:
        print("文件编码错误:", e)
