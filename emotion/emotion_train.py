# coding=utf-8

import pandas as pd
import numpy as np
import re
import jieba.posseg as psg
from PIL import Image
from matplotlib import pyplot as plt
from sqlalchemy import create_engine
from sqlalchemy import text
import os

from sqlalchemy.orm import sessionmaker
from wordcloud import WordCloud

from util.query import querys

current_path = os.path.dirname(os.path.abspath(__file__))

engine = create_engine('mysql+pymysql://root:123456@localhost/dbm')
con = engine.connect()


def get_pos_and_neg_data():
    # 读入正面、负面情感评价词 生成 dictionary.py文件
    pos_comment = pd.read_csv(current_path + "/语录/正面评价词语（中文）.txt", header=None, sep="/n", engine='python',
                              encoding='gbk')
    neg_comment = pd.read_csv(current_path + "/语录/负面评价词语（中文）.txt", header=None, sep="/n", engine='python',
                              encoding='gbk')
    pos_emotion = pd.read_csv(current_path + "/语录/正面情感词语（中文）.txt", header=None, sep="/n", engine='python',
                              encoding='gbk')
    neg_emotion = pd.read_csv(current_path + "/语录/负面情感词语（中文）.txt", header=None, sep="/n", engine='python',
                              encoding='gbk')

    # 合并情感词与评价词
    positive = set(pos_comment.iloc[:, 0]) | set(pos_emotion.iloc[:, 0])
    negative = set(neg_comment.iloc[:, 0]) | set(neg_emotion.iloc[:, 0])
    # 正负面情感词表中相同的词语
    intersection = positive & negative
    # 去掉相同的词
    positive = list(positive - intersection)
    negative = list(negative - intersection)
    # 正面词语赋予初始权重1，负面词语赋予初始权重-1
    positive = pd.DataFrame({"word": positive,
                             "weight": [1] * len(positive)})
    negative = pd.DataFrame({"word": negative,
                             "weight": [-1] * len(negative)})
    posneg = pd.concat([positive, negative], ignore_index=True)
    posneg.to_csv(current_path + "/dictionary.csv", index=False, encoding='utf-8')
    return posneg


def emotion_posess(reviews, sid):
    # 评论去重
    # reviews[['comment_cotent', 'comment_stat']].duplicated().sum()
    reviews = reviews[['comment_cotent', 'comment_stat', 'comment_time']].drop_duplicates()
    reviews.reset_index(drop=True, inplace=True)
    # print(reviews)

    content = reviews['comment_cotent']
    # 编译匹配模式
    # 去掉评论中的数字、字母，以及“京东”“京东商城”“美的”“热水器”“电热水器"
    pattern = re.compile('[a-zA-Z0-9]|景区|景点|很|都|去')
    # re.sub用于替换字符串中的匹配项
    content = content.apply(lambda x: pattern.sub('', x))
    # print(content)
    # 自定义简单的分词函数
    worker = lambda s: [[x.word, x.flag] for x in psg.cut(s)]  # 单词与词性
    seg_word = content.apply(worker)
    # print(seg_word)
    # 将词语转化为数据框形式，一列是词，一列是词语所在的句子id，最后一列是词语在该句子中的位置
    # 每一评论中词的个数
    n_word = seg_word.apply(lambda x: len(x))
    # 构造词语所在的句子id
    n_content = [[x + 1] * y for x, y in zip(list(seg_word.index), list(n_word))]
    # 将嵌套的列表展开，作为词所在评论的id
    index_content = sum(n_content, [])

    seg_word = sum(seg_word, [])
    # 词
    word = [x[0] for x in seg_word]
    # 词性
    nature = [x[1] for x in seg_word]
    # content_type评论类型
    content_type = [[x] * y for x, y in zip(list(reviews['comment_stat']), list(n_word))]
    content_type = sum(content_type, [])
    # comment_time 评论时间
    content_time = [[x] * y for x, y in zip(list(reviews['comment_time']), list(n_word))]
    content_time = sum(content_time, [])
    # 构造数据框
    result = pd.DataFrame({'index_content': index_content,
                           'word': word,
                           'nature': nature,
                           'content_type': content_type,
                           'content_time': content_time})
    # 删除标点符号
    result = result[result['nature'] != 'x']
    # 删除停用词
    # 加载停用词
    stop_path = open(current_path + '/语录/hit_stopwords.txt', 'r', encoding='utf-8')
    stop = [x.replace('\n', '') for x in stop_path.readlines()]
    # 得到非停用词序列
    word = list(set(word) - set(stop))
    # 判断表格中的单词列是否在非停用词列中
    result = result[result['word'].isin(word)]
    # 构造各词在评论中的位置列
    n_word = list(result.groupby(by=['index_content'])['index_content'].count())
    index_word = [list(np.arange(0, x)) for x in n_word]
    index_word = sum(index_word, [])
    result['index_word'] = index_word
    result.reset_index(drop=True, inplace=True)
    # 提取含名词的评论的句子id
    ind = result[[x == 'n' for x in result['nature']]]['index_content'].unique()
    # 提取评论
    result = result[result['index_content'].isin(ind)]
    # 重置索引
    result.reset_index(drop=True, inplace=True)
    # 读入评论词表
    word = result

    posneg = pd.read_csv(current_path + "/dictionary.csv")
    data_posneg = pd.merge(left=word, right=posneg, on='word', how='left')
    # 先按评论id排序，再按在评论中的位置排序
    data_posneg = data_posneg.sort_values(by=['index_content', 'index_word'])
    # 根据情感词前面两个位置的词语是否存在否定词或双层否定词对情感值进行修正
    # 载入否定词表
    notdict = pd.read_csv(current_path + "/语录/not.csv")
    # 处理否定修饰词
    # 构造新列，作为经过否定词修正后的情感值
    data_posneg['amend_weight'] = data_posneg['weight']
    data_posneg['id'] = np.arange(0, len(data_posneg))
    # 只保留有情感值的词语
    only_inclination = data_posneg.dropna()
    # 修改索引
    only_inclination.index = np.arange(0, len(only_inclination))
    index = only_inclination['id']
    for i in np.arange(0, len(only_inclination)):
        # 提取第i个情感词所在的评论
        review = data_posneg[data_posneg['index_content'] == only_inclination['index_content'][i]]
        # 修改索引
        review.index = np.arange(0, len(review))
        # 第i个情感值在该文档的位置
        affective = only_inclination['index_word'][i]
        if affective == 1:
            # 情感词前面的单词是否在否定词表
            ne = sum([i in notdict['term'] for i in review['word'][affective - 1]])
            if ne == 1:
                data_posneg['amend_weight'][index[i]] = -data_posneg['weight'][index[i]]
        elif affective > 1:
            # 情感词前面两个位置的词语是否在否定词，存在一个调整成相反的情感权重，存在两个就不调整
            ne = sum([i in notdict['term'] for i in review['word'][[affective - 1, affective - 2]]])
            if ne == 1:
                data_posneg['amend_weight'][index[i]] = -data_posneg['weight'][index[i]]

    # 计算每条评论的情感值
    emotional_value = only_inclination.groupby(['index_content', 'content_time'], as_index=False)['amend_weight'].sum()
    emotional_score = emotional_value
    score_time_pd = emotional_score[['content_time', 'amend_weight']]
    score_time_pd.to_csv(current_path + f"/datas/score_data/{sid}.csv", index=False, encoding='utf-8')

    # 去除情感值为0的评论
    emotional_value = emotional_value[emotional_value['amend_weight'] != 0]
    emotional_value.reset_index(drop=True, inplace=True)
    # 给情感值大于0的赋予评论类型pos，小于0的赋予neg
    emotional_value['a_type'] = ''
    emotional_value.loc[emotional_value.amend_weight > 0, 'a_type'] = '好评'
    emotional_value.loc[emotional_value.amend_weight < 0, 'a_type'] = '差评'
    # emotional_value.loc[emotional_value.amend_weight == 0, 'a_type'] = '中评'
    # 查看情感分析的结果
    result = pd.merge(left=word, right=emotional_value, on='index_content', how='right')
    # 删除中评
    result = result[result['content_type'] != '中评']
    # 混淆矩阵-交叉表
    confusion_matrix = pd.crosstab(result['content_type'], result['a_type'], margins=True)
    accuracy = (confusion_matrix.iloc[0, 0] + confusion_matrix.iloc[1, 1]) / confusion_matrix.iloc[2, 2]
    # print(accuracy)
    # 提取正负面评论信息
    # 得到正面评论与负面评论对应的索引
    ind_pos = list(emotional_value[emotional_value['a_type'] == '好评']['index_content'])
    ind_neg = list(emotional_value[emotional_value['a_type'] == '差评']['index_content'])
    # 得到正面评论与负面评论
    posdata = word[[i in ind_pos for i in word['index_content']]]
    negdata = word[[i in ind_neg for i in word['index_content']]]
    # 将结果写出,每条评论作为一行
    posdata.to_csv(current_path + f"/datas/pos/{sid}_posdata.csv", index=False, encoding='utf-8')
    negdata.to_csv(current_path + f"/datas/neg/{sid}_negdata.csv", index=False, encoding='utf-8')
    return posdata, negdata


def create_pos_img(posdata, sid):
    # 绘制正面情感词云
    # 正面情感词词云
    freq_pos = posdata.groupby(by=['word'])['word'].count()
    freq_pos = freq_pos.sort_values(ascending=False)
    # 从文件中将图像读取为数组
    img = Image.open(current_path + '/111.jpg')
    backgroud_Image = np.array(img)
    wordcloud = WordCloud(font_path=current_path + "/msyh.ttc",  # 这里的字体要与自己电脑中的对应
                          max_words=200,  # 选择前100词
                          background_color='white',  # 背景颜色为白色
                          mask=backgroud_Image)
    pos_wordcloud = wordcloud.fit_words(freq_pos)
    # 将数据展示到二维图像上
    plt.imshow(pos_wordcloud)
    # 关掉x,y轴
    plt.axis('off')
    path = current_path + f'/datas/pos_img/{sid}'
    plt.savefig(path)
    plt.close()


def create_neg_img(negdata, sid):
    # 绘制负面情感词云
    # 负面情感词词云
    # print(negdata)
    freq_neg = negdata.groupby(by=['word'])['word'].count()
    freq_neg = freq_neg.sort_values(ascending=False)

    # 从文件中将图像读取为数组
    img = Image.open(current_path + '/111.jpg')
    backgroud_Image = np.array(img)
    wordcloud = WordCloud(font_path=current_path + "/msyh.ttc",  # 这里的字体要与自己电脑中的对应
                          #                       max_words=200,            # 选择前100词
                          background_color='white',  # 背景颜色为白色
                          mask=backgroud_Image)
    neg_wordcloud = wordcloud.fit_words(freq_neg)
    # 将数据展示到二维图像上
    plt.imshow(neg_wordcloud)
    # 关掉x,y轴
    plt.axis('off')  # 关闭x,y轴
    path = current_path + f'/datas/neg_img/{sid}'
    plt.savefig(path)
    plt.close()


def start_emotion_train(sid):
    score_src = current_path + f"/datas/score_data/{sid}.csv"
    posImg_src = current_path + f"/datas/pos_img/{sid}.png"
    negImg_src = current_path + f"/datas/neg_img/{sid}.png"
    if os.path.exists(current_path + f'/datas/neg_img/{sid}.png') and os.path.exists(
            current_path + f'/datas/pos_img/{sid}.png'):
        return posImg_src, negImg_src, score_src
    else:
        sql_1 = f'select comment_cotent,comment_stat,comment_time from comments WHERE sid = {sid};'
        reviews = pd.read_sql(text(sql_1), con=con)
        posdata, negdata = emotion_posess(reviews, sid)
        create_pos_img(posdata, sid)
        create_neg_img(negdata, sid)
        return posImg_src, negImg_src, score_src


if __name__ == '__main__':
    sid = 1394
    print(start_emotion_train(sid))
    # get_pos_and_neg_data()
    # print(current_path)
