import random
from numpy import mean
from util.utils import *
import requests


def get_province_map(type):
    df_map = pd.read_csv('./province.csv')
    province = df_map.loc[df_map['type'].str.contains(type)]['name'].values[0]
    map_url = df_map.loc[df_map['type'].str.contains(type)]['url'].values[0]
    # print(province)
    # print(map_url)
    return province, map_url


def get_city_name(map_url):
    headers = {
        'user-agent': 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }
    res = requests.get(map_url, headers=headers)
    res_data = res.json()
    features = res_data.get('features')
    city_name = []
    for feature in features:
        city_name.append(feature.get('properties').get('name'))
    return city_name


def get_province_data(type):
    # 获取type的城市的景点数量
    province, map_url = get_province_map(type)
    city_names = get_city_name(map_url)
    sids = list(df_travel.loc[df_travel['address'].str.contains(type)]['sid'])
    province_data = list()
    for sid in sids:
        adddress = list(map(lambda x: x.split(','), df_travel.loc[df_travel['sid'] == sid]['address'].values))[0]
        if len(adddress) > 1:
            province_data.append(adddress[1])
    typesObj = {}
    for i in province_data:
        if typesObj.get(i, -1) == -1:
            typesObj[i] = 1
        else:
            typesObj[i] += 1
    max_num = max(typesObj.values()) if typesObj else 0
    city_datas = []
    for key, item in typesObj.items():
        for city in city_names:
            if key in city:
                city_datas.append({
                    "name": city,
                    "value": item
                })
    return city_datas, max_num


def get_city_scenic_price(type):
    # 按省份获取平均满意度和平均价格
    df_2 = df_travel
    df_2.drop_duplicates(subset=['sid'], keep='first', inplace=True)
    address_list = list(map(lambda x: x.split(','), df_2.loc[df_2['address'].str.contains(type)]['address']))
    province_data = set()
    for adddress in address_list:
        if len(adddress):
            province_data.add(adddress[-1])
    cityList = list(province_data)
    price_obj = []
    degree_obj_list = []
    city_obj = cityList
    for i in cityList:
        degreeLevel = list(df_2.loc[df_2['address'].str.contains(i)]['degreeLevel'])
        degreeLevel_int = list(map(lambda x: int(x) if x else 0, degreeLevel))
        degree_avg = round(mean(degreeLevel_int), 2)
        degree_obj_list.append(degree_avg)
        price = list(df_2.loc[df_2['address'].str.contains(i)]['price'])
        price_int = list(map(lambda x: float(x) if x else 0, price))
        price_avg = round(mean(price_int), 2)
        price_obj.append(price_avg)
    degree_obj = []
    for i, j in zip(city_obj, degree_obj_list):
        degree_obj.append({
            'value': j,
            'name': i
        })
    # print(degree_obj)
    degree_list = sorted(degree_obj, key=lambda x: x.get('value'), reverse=True)

    return city_obj, degree_obj_list, price_obj, degree_list


def get_city_heat_data(type):
    # 根据省份获取热度top6景区
    totalNum_str = list(df_travel.loc[df_travel['address'].str.contains(type)]['totalNum'])
    totalNum = list(map(lambda x: int(x) if x else 0, totalNum_str))
    title = list(df_travel.loc[df_travel['address'].str.contains(type)]['title'])
    data_obj = {}
    for i, j in zip(totalNum, title):
        data_obj[j] = i
    data_list = sorted(data_obj.items(), key=lambda x: x[1], reverse=True)
    heat_data_obj = []
    for i in data_list[:6]:
        heat_data_obj.append({"value": i[1], "name": i[0]})
    # # print(heat_data_obj)
    # print(data_list)
    return heat_data_obj, data_list


def get_city_scenie_stat(type):
    # 根据省份获取景区的星级数
    stats = list(df_travel.loc[df_travel['address'].str.contains(type)]['level'])
    stat_cnt = len(stats)
    five_cnt, four_cnt, three_cnt, other_cnt = 0, 0, 0, 0
    for s in stats:
        if '5A' in s:
            five_cnt += 1
        elif '4A' in s:
            four_cnt += 1
        elif '3A' in s:
            three_cnt += 1
        else:
            other_cnt += 1
    city_scenic_stat_obj = [
        {
            "name": '5A景区',
            "value": five_cnt,
        }, {
            "name": '4A景区',
            "value": four_cnt,
        }, {
            "name": '3A景区',
            "value": three_cnt,
        }, {
            "name": '其他',
            "value": other_cnt,
        },
    ]
    return city_scenic_stat_obj, stat_cnt


def get_city_scenie_comment_level(type):
    # 根据省份获取景区的好评与差评  按热度排序
    df_temp = df_travel
    sids = list(set(df_temp.loc[df_temp['address'].str.contains(type)]['sid']))
    df_temp['totalNum'] = df_temp['totalNum'].astype(int)
    totalNum_dict = {}
    for sid in sids:
        totalNum = df_temp[df_temp['sid'] == sid]['totalNum'].values
        goodNum = df_temp[df_temp['sid'] == sid]['goodNum'].values
        badNum = df_temp[df_temp['sid'] == sid]['badNum'].values
        if not list(totalNum):
            continue
        else:
            name = df_temp[df_temp['sid'] == sid]['title'].values[0]
            totalNum_dict[totalNum[0]] = [name, goodNum[0], badNum[0]]
    totalNum_list = sorted(totalNum_dict.items(), key=lambda x: x[0], reverse=True)
    # print(totalNum_list)
    goodNum_lsit = list()
    badNum_lsit = list()
    title_lsit = list()
    for _, i in totalNum_list[:6]:
        title_lsit.append(i[0])
        goodNum_lsit.append(i[1])
        badNum_lsit.append(i[2])
    # print(title_lsit)
    # print(goodNum_lsit)
    # print(badNum_lsit)
    return title_lsit, goodNum_lsit, badNum_lsit


def get_city_service_score(types):
    # 根据省份获取该省的所有景区的服务评价平均值
    if types == 'all':
        serviceScoreAvgLists = list(df_travel['serviceScoreAvgList'].values)
    else:
        serviceScoreAvgLists = list(df_travel.loc[df_travel['address'].str.contains(types)]['serviceScoreAvgList'])
    # print(serviceScoreAvgLists)
    service1, service2, service3, service4 = [], [], [], []
    for serviceScoreAvgStr in serviceScoreAvgLists:
        serviceScorelist = eval(serviceScoreAvgStr)
        # print(serviceScorelist)
        if not serviceScorelist: continue
        for serviceScore in serviceScorelist:
            if serviceScore.get('serviceName') == '同程服务':  # 同程服务
                service1.append(int(serviceScore.get('score')))
            elif serviceScore.get('serviceName') == '产品便捷':  # 产品便捷
                service2.append(int(serviceScore.get('score')))
            elif serviceScore.get('serviceName') == '性价比':  # 性价比
                service3.append(int(serviceScore.get('score')))
            elif serviceScore.get('serviceName') == '景区体验':  # 景区体验
                service4.append(int(serviceScore.get('score')))
    # print(service1, service2, service3, service4)
    service1_avg = round(mean(service1), 1)
    service2_avg = round(mean(service2), 1)
    service3_avg = round(mean(service3), 1)
    service4_avg = round(mean(service4), 1)
    serviceObj = {
        '同程服务': service1_avg,
        '产品便捷': service2_avg,
        '性价比': service3_avg,
        '景区体验': service4_avg,
    }
    return list(serviceObj.values())


def get_city_heat_sort(types):
    # 根据省份获取市的旅游热度
    df_temp = df_travel
    df_temp['totalNum'] = df_temp['totalNum'].astype(int)
    address_list = list(map(lambda x: x.split(','), df_temp.loc[df_temp['address'].str.contains(types)]['address']))
    province_data = set()
    for adddress in address_list:
        if len(adddress):
            province_data.add(adddress[-1])
    cityList = list(province_data)
    totalNum_obj = {}
    for i in cityList:
        totalNumList = list(df_temp.loc[df_temp['address'].str.contains(i)]['totalNum'])
        totalNum_obj[i] = sum(totalNumList)
    # print(totalNum_obj)
    city_name = list(totalNum_obj.keys())
    total_num = list(totalNum_obj.values())
    return city_name, total_num


def process_city_heat_data(types):
    city_name, total_num = get_city_heat_sort(types)
    new_total_num_obj = {}
    for total, city in zip(total_num, city_name):
        j = 0
        new_total_num = []
        for i in range(10):
            r = random.randint(total // 12, total // 10)
            j += r
            new_total_num.append(j)
        new_total_num.append(total)
        new_total_num.sort(reverse=True)
        new_total_num_obj[city] = new_total_num
    # print(new_total_num_obj)
    data_list = sorted(new_total_num_obj.items(), key=lambda x: x[1][-1], reverse=True)
    change_data = []
    # print(data_list)
    for i in range(11):
        temp = []
        for j in data_list[:6]:
            temp.append(j[1][i])
        # print(temp)
        change_data.append(temp)
    # print(change_data)
    city_name_top6 = [i[0] for i in data_list[:6]]
    # print(city_name_top6)
    return change_data, city_name_top6


if __name__ == '__main__':
    # print(get_province_map('四川'))
    # print(get_province_data('四川'))
    # types = '四川'
    # print(process_city_heat_data('四川'))
    print(get_province_data('四川'))
    # print(get_province_map('广东'))
    # province, map_url= get_province_map('广东')
    # print(province, map_url)
    # print(get_city_name(map_url))
