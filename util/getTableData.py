# encoding=utf-8
from travel.util.utils import *
from travel.util.query import *


def delMovieByMovieName(movieName):
    sql = 'delete from movie where title = %s'
    querys(sql, [movieName])
    return '删除成功'


def getTableDataBYTablePage():
    sql = 'select id,sid,title,detail_link,main_img,address,`level`,feature,price,video,totalNum,degreeLevel from travel'
    result = querys(sql, [], 'select')
    data = []
    for row in result:
        d = {}
        d['id'] = row[0]
        d['sid'] = row[1]
        d['title'] = row[2]
        d['detail_link'] = row[3]
        d['main_img'] = row[4]
        d['address'] = row[5]
        d['level'] = row[6]
        d['feature'] = row[7]
        d['price'] = row[8]
        d['video'] = row[9]
        d['totalNum'] = row[10]
        d['degreeLevel'] = row[11]
        data.append(d)
    return data
'''
<tr>
        <th>ID</th>
        <th>景点</th>
        <th>图片</th>
        <th>等级</th>
        <th>价格</th>
        <th>特色</th>
        <th>地区</th>
        <th>评论数</th>
        <th>满意度</th>
        <th>视频</th>
        <th>操作</th>
    </tr>

'''

def getMovierUrlById(videoId):
    tableDate = df_travel[df_travel['sid'] == int(videoId)]['video'].values
    return tableDate[0]


if __name__ == '__main__':
    # print(getTableDataBYTablePage())
    print(getTableDataBYTablePage())