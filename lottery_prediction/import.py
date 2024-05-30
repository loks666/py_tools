import pandas as pd
import pymysql

# 创建数据库连接
conn = pymysql.connect(host='localhost', port=3306, user='root', password='Lx284190056', db='lottery')


# 定义一个函数来处理数据
def process_data(data):
    # 根据你提供的数据样本，每个字段的长度如下：
    field_lengths = [5, 2, 2, 2, 2, 2, 2, 2, 13, 11, 3, 8, 12, 10, 10]
    fields = []
    start = 0
    for length in field_lengths:
        fields.append(data[start:start + length].strip())
        start += length
    return fields


# 读取txt文件
with open('彩票.txt', 'r') as f:
    lines = f.readlines()

# 处理数据并创建DataFrame
data = []
for line in lines:
    data.append(process_data(line))
print(data)
df = pd.DataFrame(data, columns=['期号', '红1', '红2', '红3', '红4', '红5', '红6', '蓝球', '奖池奖金(元)', '一等奖注数',
                                 '一等奖金(元)', '二等奖注数', '二等奖金(元)', '总投注额(元)', '开奖日期'])

print(df)
# 将数据插入到数据库
# df.to_sql('双色球', conn, if_exists='append', index=False)

# 关闭数据库连接
# conn.close()
