from flask import request, render_template, session, redirect, Blueprint, jsonify

from redis_cache import cache
from util.getHomeData import *
from util.getChinaData import *
from util.getDataShow import *
from util.getProvinceData import *
from util.getProvinceMap import *
from util.getTableData import *
from util.getSearchData import *

from util.getTrafficData import *

dataShow = Blueprint('dataShow', __name__)


@dataShow.route('/home', methods=['GET', 'POST'])
@cache.cached(timeout=300)
def home():  # put application's code here
    email = session.get('email')
    name = session.get('name')
    dataList, years, cnt_pay, towns_pay, village_pay, speed_up = get_data_chart1()
    years_chart2, data_obj = get_data_chart2()
    entry_visitors, entry_visitors_foreign, entry_visitors_hk_macao, entry_visitors_taiwan = get_data_chart3()
    years_chart3 = years_chart2[::-1]
    table_titles, table_years, table_data = get_data_table()
    return render_template('index.html', name=name, email=email,
                           dataList=dataList, years=years, cnt_pay=cnt_pay, towns_pay=towns_pay,
                           village_pay=village_pay,
                           speed_up=speed_up,
                           years_chart2=years_chart2, data_obj=data_obj,
                           years_chart3=years_chart3[:-3], entry_visitors=entry_visitors,
                           entry_visitors_foreign=entry_visitors_foreign,
                           entry_visitors_hk_macao=entry_visitors_hk_macao, entry_visitors_taiwan=entry_visitors_taiwan,
                           table_titles=table_titles, table_years=table_years, table_data=table_data,
                           )


@dataShow.route('/data_show/<type>', methods=['GET', 'POST'])
def data_show(type):
    email = session.get('email')
    if not email:
        return redirect('/login')
    name = session.get('name')
    scenic_count = get_scenic_count()
    if type == 'all':
        typesList = get_province_type()
        # print(typeList)
        return render_template('data_show.html', email=email, name=name,
                               typesList=typesList)
    elif type == 'china':
        area = '全国'
        china_datas = get_china_data()
        row_chart1, col_chart1 = get_price()
        # row_chart2, col_chart2, full_list, persen = get_provien_scenic()
        scenic_stat_obj, all_cnt = get_scenic_stat()
        degree_obj = get_degreeLevel()
        top6_data = get_heat_data()
        heat_province_row, heat_province_col = get_heat_data_by_province()
        hear_max = max(heat_province_col)
        serviceObjkeys = get_city_service_score('all')
        return render_template('china_show.html', email=email, name=name, datas=china_datas,
                               count=scenic_count, type=area,
                               row_chart1=row_chart1, col_chart1=col_chart1,
                               # row_chart2=row_chart2[:6], col_chart2=col_chart2[:6], full_list=full_list[:6],
                               # persen=persen[:6],
                               serviceObjkeys=serviceObjkeys,
                               scenic_stat_obj=scenic_stat_obj, all_cnt=all_cnt,
                               degree_obj=degree_obj,
                               top6_data=top6_data,
                               heat_province_row=heat_province_row, heat_province_col=heat_province_col,
                               hear_max=hear_max,
                               )
    else:
        scenic_cnt, totalNum = get_province_bytype(type)
        province, map_url = get_province_map(type)
        dataList, max_num = get_province_data(type)
        # print(dataList)
        # print(province)
        city_obj, degree_obj, price_obj, _ = get_city_scenic_price(type)
        heat_data_obj, _ = get_city_heat_data(type)
        city_scenic_stat_obj, stat_cnt = get_city_scenie_stat(type)
        title_lsit, goodNum_lsit, badNum_lsit = get_city_scenie_comment_level(type)
        serviceObjkeys = get_city_service_score(type)
        change_data, city_name_top6 = process_city_heat_data(type)
        return render_template('province_show.html', email=email, name=name,
                               scenic_cnt=scenic_cnt, totalNum=totalNum, type=type, max_num=max_num,
                               province=province, map_url=map_url, dataList=dataList,
                               city_obj=city_obj, degree_obj=degree_obj, price_obj=price_obj,
                               heat_data_obj=heat_data_obj, city_scenic_stat_obj=city_scenic_stat_obj,
                               stat_cnt=stat_cnt,
                               title_lsit=title_lsit, goodNum_lsit=goodNum_lsit, badNum_lsit=badNum_lsit,
                               serviceObjkeys=serviceObjkeys, change_data=change_data, city_name_top6=city_name_top6,
                               )


@dataShow.route('/table/<scenicName>')
def table(scenicName):
    email = session.get('email')
    name = session.get('name')
    # redis_key = 'user:{}:profile'.format(email)
    # ret_data = cache.get(redis_key)
    # # print(ret_data)
    # if ret_data:
    #     tableData = ret_data
    # else:
    #     tableData = getTableDataBYTablePage()
    #     tableData = list(tableData)
    #     cache.set(redis_key, tableData)
    # if scenicName != '0':
    #     # 删除
    #     delMovieByMovieName(scenicName)
    #     return redirect('/table/0')
    return render_template('table.html', email=email,
                           name=name)


@dataShow.route('/jsondata', methods=['GET'])
def get_tabel_data():
    info = request.values
    limit = info.get('limit', 10)  # 每页显示的条数
    offset = info.get('offset', 0)  # 分片数，(页码-1)*limit，它表示一段数据的起点
    data = getTableDataBYTablePage()

    return jsonify({'total': len(data), 'rows': data[int(offset):(int(offset) + int(limit))]})
    # 注意total与rows是必须的两个参数，名字不能写错，total是数据的总长度，rows是每页要显示的数据,它是一个列表
    # 前端根本不需要指定total和rows这俩参数，他们已经封装在了bootstrap table里了


@dataShow.route('/video/<int:videoId>')
def movie(videoId):
    videoUrl = getMovierUrlById(videoId)
    return render_template('video.html', videoUrl=videoUrl)


@dataShow.route('/search/<int:searchId>', methods=['GET', 'POST'])
def search(searchId):
    email = session.get('email')
    name = session.get('name')
    if request.method == 'GET':
        resultData = getDeatailById(searchId)
    else:
        request.form = dict(request.form)
        resultData = getDeatailBySearchById(request.form['searchName'])
    return render_template('search.html', name=name, email=email, resultData=resultData)


@dataShow.route('/traffic/<city>', methods=['GET', 'POST'])
def traffic(city):
    email = session.get('email')
    name = session.get('name')
    if request.method == 'GET':
        if city == 'all':
            city = '广州'
        row_data1, col_data1, row_data2, col_data2, row_data3, col_data3, row_data4, col_data4 = get_traffic_index(city)
        item_obj = get_traffic_district_data(city)
        roadrank_obj = get_traffic_roadrank_data(city)
        mapdata, center = get_map_data(city)
    else:
        city = dict(request.form)['cityName']
        row_data1, col_data1, row_data2, col_data2, row_data3, col_data3, row_data4, col_data4 = get_traffic_index(city)
        item_obj = get_traffic_district_data(city)
        roadrank_obj = get_traffic_roadrank_data(city)
        mapdata, center = get_map_data(city)
    return render_template('traffic.html', name=name, email=email,city=city,
                           row_chart1=row_data1, col_chart1=col_data1,
                           row_chart2=row_data2, col_chart2=col_data2,
                           row_chart3=row_data3, col_chart3=col_data3,
                           row_chart4=row_data4, col_chart4=col_data4,
                           item_obj1=item_obj[0], item_obj2=item_obj[1], item_obj3=item_obj[2],
                           roadrank_obj=roadrank_obj, mapdata=mapdata, center=center,
                           )


if __name__ == '__main__':
    data_show('all')
