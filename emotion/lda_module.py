import itertools
from gensim import corpora, models
from matplotlib import pyplot as plt
import pyLDAvis.gensim
import re
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sqlalchemy import text
import os



'''
pandas==1.2.4
numpy==1.22.3
gensim==4.2.0  (python==3.10)
'''
current_path = os.path.dirname(os.path.abspath(__file__))
engine = create_engine('mysql+pymysql://root:123456@localhost/dbm')
con = engine.connect()

def cos(vector1, vector2):
    """
    计算两个向量的余弦相似度函数
    :param vector1:
    :param vector2:
    :return: 返回两个向量的余弦相似度
    """
    dot_product = 0.0
    normA = 0.0
    normB = 0.0
    for a, b in zip(vector1, vector2):
        dot_product += a * b
        normA += a ** 2
        normB += b ** 2
    if normA == 0.0 or normB == 0.0:
        return (None)
    else:
        return (dot_product / ((normA * normB) ** 0.5))


def lda_k(x_corpus, x_dict):
    """
    主题数寻优
    :param x_corpus: 语料库
    :param x_dict: 词典
    :return:
    """
    # 初始化平均余弦相似度
    mean_similarity = []
    mean_similarity.append(1)

    # 循环生成主题并计算主题间相似度
    for i in np.arange(2, 11):
        lda = models.LdaModel(x_corpus, num_topics=i, id2word=x_dict)  # LDA模型训练
        for j in np.arange(i):
            term = lda.show_topics(num_words=50)

        # 提取各主题词
        top_word = []
        for k in np.arange(i):
            top_word.append([''.join(re.findall('"(.*)"', i)) for i in term[k][1].split('+')])  # 列出所有词

        # 构造词频向量
        word = sum(top_word, [])  # 列出所有的词
        unique_word = set(word)  # 去除重复的词

        # 构造主题词列表，行表示主题号，列表示各主题词
        mat = []
        for j in np.arange(i):
            top_w = top_word[j]
            mat.append(tuple([top_w.count(k) for k in unique_word]))

        p = list(itertools.permutations(list(np.arange(i)), 2))
        l = len(p)
        top_similarity = [0]
        for w in np.arange(l):
            vector1 = mat[p[w][0]]
            vector2 = mat[p[w][1]]
            top_similarity.append(cos(vector1, vector2))

        # 计算平均余弦相似度
        mean_similarity.append(sum(top_similarity) / l)
    return (mean_similarity)


def draw_model(pos_k, neg_k):
    # 绘制主题平均余弦相似度图形
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    # 中文乱码解决方法
    plt.rcParams['font.family'] = ['Arial Unicode MS', 'Microsoft YaHei', 'SimHei', 'sans-serif']
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号 #有中文出现的情况，需要u'内容'
    fig = plt.figure(figsize=(10, 8))
    ax1 = fig.add_subplot(211)
    ax1.plot(pos_k)
    ax1.set_xlabel('正面评论LDA主题数寻优', fontsize=14)
    ax2 = fig.add_subplot(212)
    ax2.plot(neg_k)
    ax2.set_xlabel('负面评论LDA主题数寻优', fontsize=14)
    plt.show()


def create_model(sid):
    # 载入情感分析后的数据
    pos_path = current_path + f'/datas/pos/{sid}_posdata.csv'
    neg_path = current_path + f'/datas/neg/{sid}_negdata.csv'
    posdata = pd.read_csv(pos_path, encoding='utf-8')
    negdata = pd.read_csv(neg_path, encoding='utf-8')
    # 建立词典
    pos_dict = corpora.Dictionary([[i] for i in posdata['word']])  # 正面
    neg_dict = corpora.Dictionary([[i] for i in negdata['word']])  # 负面
    # 建立语料库
    pos_corpus = [pos_dict.doc2bow(j) for j in [[i] for i in posdata['word']]]  # 正面
    neg_corpus = [neg_dict.doc2bow(j) for j in [[i] for i in negdata['word']]]  # 负面
    # 计算主题平均余弦相似度
    pos_k = lda_k(pos_corpus, pos_dict)
    neg_k = lda_k(neg_corpus, neg_dict)
    # print('正面评论主题的平均相似度', pos_k)
    # print('负面评论主题的平均相似度', neg_k)
    pos_topics = pos_k.index(min(pos_k))
    neg_topics = neg_k.index(min(neg_k))
    # 用图来看模型,选择主题树
    # draw_model(pos_k,neg_k)
    pos_lda = models.LdaModel(pos_corpus, num_topics=2, id2word=pos_dict)
    pos_lda_theme = pos_lda.print_topics(num_words=10)
    # print(pos_lda_theme)
    neg_lda = models.LdaModel(neg_corpus, num_topics=2, id2word=neg_dict)
    neg_lda_theme = neg_lda.print_topics(num_words=10)
    # print(neg_lda_theme)
    return [pos_lda, pos_corpus, pos_dict], [neg_lda, neg_corpus, neg_dict]


def display_theme(lda):
    theme = lda.show_topics()
    # 取出高频词
    pattern = re.compile(r'[\u4e00-\u9fa5]+')
    key_words = []
    index = []
    for i in range(2):
        key_words.append(pattern.findall(theme[i][1]))
        index.append(f'主题{i + 1}')
    key_words_list = pd.DataFrame(data=key_words, index=index)
    print(key_words_list)
    return key_words_list


def display_LDA(data_list, sid, flag):
    if not os.path.exists('LDA_model'):
        os.mkdir('LDA_model')
    path = current_path + f'/LDA_model/{sid}_{flag}_LDA.html'
    lda = data_list[0]
    data_corpus = data_list[1]
    data_dict = data_list[2]
    vis = pyLDAvis.gensim.prepare(lda, data_corpus, data_dict, mds='mmds')
    pyLDAvis.save_html(vis, path)
    return path


def LDA_start(searchName):
    sql = f'select sid from travel WHERE title like "%{searchName}%" limit 5000'
    sid_pd = pd.read_sql(text(sql), con=con)
    if sid_pd.empty:
        return '', ''
    sid = sid_pd['sid'].tolist()[0]
    pos_path = current_path + f'/LDA_model/{sid}_pos_LDA.html'
    neg_path = current_path + f'/LDA_model/{sid}_neg_LDA.html'
    if os.path.exists(pos_path) and os.path.exists(neg_path):
        return pos_path, neg_path, sid
    else:
        pos_list, neg_list = create_model(sid)
        display_theme(pos_list[0])
        display_theme(neg_list[0])
        pos_path = display_LDA(pos_list, sid, 'pos')
        neg_path = display_LDA(neg_list, sid, 'neg')
        return pos_path, neg_path, sid


if __name__ == '__main__':
    sid = 1394
    print(LDA_start(sid))
