#coding=utf-8
from wordcloud import STOPWORDS
from util.utils import *
import os
import jieba
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
from wordcloud import WordCloud

path = os.path.dirname(os.path.dirname(__file__))
STOPWORDS.add('特色')


def get_title_data(searchName):
    if searchName == 'all':
        title = list(df_travel['title'].values)
    else:
        title = list(df_travel[df_travel['address'].str.contains(searchName)]['title'].values)
    text = ''.join(title)
    # print(text)
    image_name = f'{searchName}_title_img'
    if not os.path.exists(path + f'/static/image/word_cloud_image/{image_name}.png'):
        resSrc = create_ciyun_image(text, image_name)
    else:
        resSrc = f'/static/image/word_cloud_image/{image_name}.png'
    return resSrc


def get_feature_data(searchName):
    if searchName == 'all':
        title = list(df_travel['feature'].values)
    else:
        title = list(df_travel[df_travel['address'].str.contains(searchName)]['feature'].values)
    text = ''.join(title)
    image_name = f'{searchName}_feature_img'
    if not os.path.exists(path + f'/static/image/word_cloud_image/{image_name}.png'):
        resSrc = create_ciyun_image(text, image_name)
    else:
        resSrc = f'/static/image/word_cloud_image/{image_name}.png'
    return resSrc




def create_ciyun_image(text, image_name):
    # 分词
    cut = jieba.cut(text)  # 切割词语
    strings = ' '.join(cut)  # 空格链接词语

    if 'feature' in image_name:
        chose = '111'
    elif 'title' in image_name:
        chose = '222'
    else:
        chose = '111'
    img = Image.open(path + f'/static/image/{chose}.png')
    img_arr = np.array(img)
    wc = WordCloud(
        background_color='#F7F7F7',  # 背景
        mask=img_arr,
        # mode='RGBA',
        stopwords=STOPWORDS.add('景区'),
        font_path=f'{path}/static/font/font_1.ttf'
    )
    wc.generate_from_text(strings)
    # 绘制图片
    flg = plt.figure(1)
    plt.imshow(wc)  # 显示词云
    plt.axis('off')  # 关闭x,y轴
    # plt.show()  # 显示
    # randomInt = random.randint(1, 100000)
    plt.savefig(f'{path}/static/image/word_cloud_image/{image_name}.png')  # 保存词云图
    return f'/static/image/word_cloud_image/{image_name}.png'




if __name__ == '__main__':
    # get_evaluate_data('云南')
    pass