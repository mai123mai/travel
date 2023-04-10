from flask import request, render_template, session, redirect, Blueprint

from redis_cache import cache
from util.getCommentData import *
from util.getCommentEmotionData import get_comment_score_data
from util.getDegreeData import *
from util.getChinaData import *
from util.getMapData import *
from util.getProvinceMap import *
from util.getSeviceData import *
from util.getPriceData import *
from util.getStarData import *
import base64

dataAnaly = Blueprint('dataAnaly', __name__)


@dataAnaly.route('/price_t/<searchName>', methods=['GET', 'POST'])
def price_t(searchName):
    email = session.get('email')
    name = session.get('name')
    row_chart1, col_chart1_1, col_chart1_2 = get_price_by_province()
    if request.method == 'GET':
        row_chart2, col_chart2_1, col_chart2_2 = getPriceDataByscenicName(searchName)
    else:
        request.form = dict(request.form)
        row_chart2, col_chart2_1, col_chart2_2 = getPriceDataByscenicName(request.form['searchName'])
    return render_template('price_t.html', email=email, name=name,
                           row_chart1=row_chart1, col_chart1_1=col_chart1_1, col_chart1_2=col_chart1_2,
                           row_chart2=row_chart2, col_chart2_1=col_chart2_1, col_chart2_2=col_chart2_2,
                           )


@dataAnaly.route('/star_t/<searchName>', methods=['GET', 'POST'])
def star_t(searchName):
    email = session.get('email')
    name = session.get('name')
    typesList = get_all_province()

    row_chart1, col_chart1 = get_star_by_province(searchName)
    if request.method == 'GET':
        scenic_stat_obj, all_cnt = get_scenic_stat()
    else:
        request.form = dict(request.form)
        searchName = request.form['searchName']
        scenic_stat_obj, all_cnt = get_city_scenie_stat(searchName)
    if searchName == 'all':
        searchName = '全国'
    return render_template('star_t.html', email=email, name=name,
                           typesList=typesList, row_chart1=row_chart1, col_chart1=col_chart1,
                           scenic_stat_obj=scenic_stat_obj, all_cnt=all_cnt, searchName=searchName,
                           )


@dataAnaly.route('/map_t/<searchName>', methods=['GET', 'POST'])
def map_t(searchName):
    email = session.get('email')
    name = session.get('name')
    typesList = get_all_province()

    change_data, city_name_list = get_map_data_chart1(searchName)
    return render_template('map_t.html', email=email, name=name, typesList=typesList,
                           change_data=change_data, city_name_list=city_name_list,
                           )


@dataAnaly.route('/degree_t/<searchName>', methods=['GET', 'POST'])
def degree_t(searchName):
    email = session.get('email')
    name = session.get('name')
    typesList = get_all_province()
    if searchName == 'all':
        degree_obj = get_degreeLevel()
        commtent_level_obj, all_cnt = get_commtent_level(searchName)
    else:
        _, _, _, degree_obj = get_city_scenic_price(searchName)
        commtent_level_obj, all_cnt = get_commtent_level(searchName)
    return render_template('degree_t.html', email=email, name=name, typesList=typesList,
                           degree_obj=degree_obj, commtent_level_obj=commtent_level_obj, all_cnt=all_cnt,
                           )


@dataAnaly.route('/heat_t/<searchName>', methods=['GET', 'POST'])
def heat_t(searchName):
    email = session.get('email')
    name = session.get('name')
    if searchName == 'all':
        heat_province_row, heat_province_col = get_heat_data_by_province()
    else:
        _, heat_data_obj = get_city_heat_data(searchName)
        heat_province_row = [i[0] for i in heat_data_obj[:10]]
        heat_province_col = [i[1] for i in heat_data_obj[:10]]
    hear_max = max(heat_province_col)

    typesList = get_all_province()
    return render_template('heat_t.html', email=email, name=name,
                           heat_province_row=heat_province_row, heat_province_col=heat_province_col, hear_max=hear_max,
                           typesList=typesList)


@dataAnaly.route('/service/<searchName>', methods=['GET', 'POST'])
def service_t(searchName):
    email = session.get('email')
    name = session.get('name')
    typesList = get_all_province()
    resSrc_title = get_title_data(searchName)
    resSrc_feature = get_feature_data(searchName)
    serviceObjkeys = get_city_service_score(searchName)
    if searchName == 'all':
        searchName = '全国'
    return render_template('service_t.html', email=email, name=name, typesList=typesList,
                           resSrc_title=resSrc_title, searchName=searchName, resSrc_feature=resSrc_feature,
                           serviceObjkeys=serviceObjkeys,
                           )


@dataAnaly.route('/comment_t/<searchName>', methods=['GET', 'POST'])
def comment_t(searchName):
    email = session.get('email')
    name = session.get('name')
    data_obj, sid_top1 = get_comment_t_top10()
    if searchName == 'all':
        searchName = sid_top1
    redis_key = 'user:{}:comment_t_data'.format(name)
    ret_data = cache.get(redis_key)
    cache.expire(redis_key, 60 * 10)
    if ret_data:
        ydata = ret_data
    else:
        ydata = get_echart1_data(searchName)
        cache.set(redis_key, ydata)
    # print(ydata)
    return render_template('comment_t.html', email=email, name=name, searchName=searchName,
                           data_obj=data_obj, ydata=ydata,
                           )


def return_img_stream(img_local_path):
    """
    工具函数:
    获取本地图片流
    :param img_local_path:文件单张图片的本地绝对路径
    :return: 图片流
    """
    with open(img_local_path, 'rb') as f:
        img_stream = base64.b64encode(f.read()).decode()
    return img_stream


@dataAnaly.route('/comment_emotion/<searchName>', methods=['GET', 'POST'])
def comment_emotion(searchName):
    email = session.get('email')
    name = session.get('name')
    if request.method == 'GET':
        searchName = "紫微洞"
    else:
        request.form = dict(request.form)
        searchName = request.form['searchName']
    ydata, posImg_src, negImg_src, = get_comment_score_data(searchName)
    posImg_stream = return_img_stream(posImg_src)
    negImg_stream = return_img_stream(negImg_src)
    return render_template('comment_emotion.html', email=email, name=name, searchName=searchName,
                           ydata=ydata, posImg_stream=posImg_stream, negImg_stream=negImg_stream,
                           )
