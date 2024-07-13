import pandas as pd
from sklearn.metrics import classification_report
from sqlalchemy import create_engine
from umap import UMAP

from bertopic import BERTopic


# 需要爬https://www.chengde.gov.cn/col/col2918/index.html
def generate_model():
    # 创建数据库连接
    engine = create_engine('mysql+pymysql://root:Lx284190056@localhost:3306/weiboarticles')

    # 从数据库中读取数据
    data = pd.read_sql_query("SELECT * FROM model_data", engine)

    # 关闭数据库连接
    engine.dispose()

    # 确保 'text' 和 'label' 字段都是字符串类型
    data['text'] = data['text'].astype(str)
    data['label'] = data['label'].astype(str)

    # 读取文本文件
    topic_model = BERTopic(calculate_probabilities=True, umap_model=UMAP(n_neighbors=5, min_dist=0.0))
    topics, probabilities = topic_model.fit_transform(data['text'])

    topic_info = topic_model.get_topic_info()
    print(topic_info)

    topic_0 = topic_model.get_topic(0)
    print(topic_0)

    topic_model.visualize_topics()
    topic_model.visualize_distribution(probabilities[0])  # 注意这里我们只可视化第一个文档的概率分布

    topic_model.save("./bertopic")
    loaded_model = BERTopic.load("./bertopic")

    predicted_labels = [str(label) for label in topics]
    true_labels = data['label']  # 这是真实的主题标签

    print(classification_report(true_labels, predicted_labels, zero_division=1))


def save_data2db():
    # 读取文本文件
    raw = pd.read_csv('../spiders/5000.txt', sep="\t")

    # 创建数据库连接
    eng = create_engine('mysql+pymysql://root:Lx284190056@localhost:3306/weiboarticles')

    # 将数据写入数据库
    raw.to_sql('model_data', con=eng, index=False, if_exists='append')

    # 关闭数据库连接
    eng.dispose()


def save_online2db():
    # 读取文本文件
    # raw = pd.read_csv('./online_shopping_10_cats.csv', sep="\t")

    # 创建数据库连接
    eng = create_engine('mysql+pymysql://root:Lx284190056@localhost:3306/weiboarticles')
    eng.execute("SELECT 1")

    # 将数据写入数据库
    # raw.to_sql('online', con=eng, index=False, if_exists='append')

    # 关闭数据库连接
    eng.dispose()


def save_south2db():
    # 读取文本文件
    raw = pd.read_csv('./南方周末关键词提取数据集.xml', sep="\t")
    # 创建数据库连接
    eng = create_engine('mysql+pymysql://root:Lx284190056@localhost:3306/weiboarticles')
    # 将数据写入数据库
    raw.to_sql('model_data', con=eng, index=False, if_exists='append')
    # 关闭数据库连接
    eng.dispose()


if __name__ == '__main__':
    save_online2db()
