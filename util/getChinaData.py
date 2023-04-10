from numpy import mean

from travel.util.utils import *
from sqlalchemy import create_engine
from sqlalchemy import text

engine = create_engine('mysql+pymysql://root:123456@localhost/dbm')
con = engine.connect()


# df = pd.read_sql(text('select * from travel'), con=con)
# df1 = pd.read_sql(text('select * from comments'), con=con)

def get_scenic_count():
    # 获取景点数量
    new_df = pd.read_sql(text('select count(*) from travel'), con=con)
    scenic_count = new_df.values[0][0]
    return scenic_count


def get_china_data():
    # 获取国内各省份的景点数
    addressList = df_travel['address'].values
    types = list(map(lambda x: x.split(','), addressList))
    typeList = list()
    for i in types:
        typeList.append(i[0])
    typesObj = {}
    for i in typeList:
        if typesObj.get(i, -1) == -1:
            typesObj[i] = 1
        else:
            typesObj[i] += 1
    proviens = ['澳门', '香港', '台湾', '新疆', '宁夏', '青海', '甘肃', '陕西', '西藏', '云南', '贵州', '四川', '重庆', '海南', '广西', '广东', '湖南',
                '湖北', '河南', '山东', '江西', '福建', '安徽', '浙江', '江苏', '上海', '黑龙江', '吉林', '辽宁', '内蒙古', '山西', '河北', '天津', '北京']
    china_datas = []
    for key, item in typesObj.items():
        if key in proviens:
            china_datas.append({
                'name': key,
                'value': item
            })
    for p in proviens:
        if p not in typesObj.keys():
            china_datas.append({
                'name': p,
                'value': 0
            })
    return china_datas


def get_price():
    # 获取各省份景点的平均价格
    addressList = df_travel['address'].values
    types = list(map(lambda x: x.split(','), addressList))
    typeList = set()
    for i in types:
        typeList.add(i[0])
    price_data = {}
    for i in typeList:
        prices = mean(list(map(lambda x: float(x), list(df_travel.loc[df_travel['address'].str.contains(i)]['price']))))
        mean_price = round(prices, 2)
        price_data[i] = mean_price
    return list(price_data.keys()), list(price_data.values())


def get_provien_scenic():
    # 获取各省份的景点数与占比
    addressList = df_travel['address'].values
    types = list(map(lambda x: x.split(','), addressList))
    typeList = list()
    for i in types:
        typeList.append(i[0])
    typesObj = {}
    for i in typeList:
        if typesObj.get(i, -1) == -1:
            typesObj[i] = 1
        else:
            typesObj[i] += 1
    full_list = [100] * len(typesObj)
    scenic_count = get_scenic_count()
    persen = [round((r / scenic_count) * 100, 1) for r in list(typesObj.values())]
    return list(typesObj.values()), list(typesObj.keys()), full_list, persen


def get_scenic_stat():
    # 获取各省份的星级景区
    addressList = df_travel['address'].values
    types = list(map(lambda x: x.split(','), addressList))
    typeList = set()
    for i in types:
        typeList.add(i[0])
    five_cnt, four_cnt, three_cnt, null_cnt = 0, 0, 0, 0
    for i in typeList:
        stat = list(df_travel.loc[df_travel['address'].str.contains(i)]['level'])
        for s in stat:
            if not s:continue
            if '5A' in s:
                five_cnt += 1
            elif '4A' in s:
                four_cnt += 1
            elif '3A' in s:
                three_cnt += 1
            else:
                null_cnt += 1
        # all_cnt = len(stat)
    # print(five_cnt, four_cnt, three_cnt, null_cnt)
    all_cnt = five_cnt + four_cnt + three_cnt + null_cnt
    scenic_stat_obj = [
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
            "value": null_cnt,
        }
    ]
    # print(scenic_stat_obj)
    # print(all_cnt)
    return scenic_stat_obj, all_cnt


def get_degreeLevel():
    # 获取各省份的景区满意度
    addressList = df_travel['address'].values
    types = list(map(lambda x: x.split(','), addressList))
    typeList = set()
    for i in types:
        typeList.add(i[0])
    degree_obj = dict()
    for i in typeList:
        degreeLevel = list(df_travel.loc[df_travel['address'].str.contains(i)]['degreeLevel'])
        degreeLevel_int = list(map(lambda x: int(x) if x else 0, degreeLevel))
        degree_avg = round(mean(degreeLevel_int), 2)
        # print(degree_avg)
        degree_obj[i] = degree_avg
    degree_list = sorted(degree_obj.items(), key=lambda x: x[1], reverse=True)
    degree_data = []
    for i in degree_list:
        degree_data.append({"value": i[1], "name": i[0]})
    return degree_data


def get_heat_data():
    # 获取热度top6
    df2 = df_travel
    df2.drop_duplicates(subset=['sid'], keep='first', inplace=True)
    df2['totalNum'] = df2['totalNum'].astype('int')
    df2 = df2.sort_values(by='totalNum', ascending=False)
    totalNum_top6 = list(df2['totalNum'].values[:6])
    title_top6 = list(df2['title'].values[:6])
    top6_data =[]
    for title, totalNum in zip(title_top6, totalNum_top6):
        top6_data_dict = {
            'name': title,
            'value': totalNum
        }
        top6_data.append(top6_data_dict)
    return top6_data


def get_heat_data_by_province():
    df2 = df_travel
    df2.drop_duplicates(subset=['sid'], keep='first', inplace=True)
    df2['totalNum'] = df2['totalNum'].astype(int)
    addressList = df2['address'].values
    types = list(map(lambda x: x.split(','), addressList))
    typeList = set()
    typesObj = {}
    for i in types:
        typeList.add(i[0])
    for type in typeList:
        totalNum = list(df2.loc[df2['address'].str.contains(type)]['totalNum'])
        totalNum_list = list(map(lambda x: int(x),totalNum))
        totalNum_count = sum(totalNum_list)
        typesObj[type] = totalNum_count
    heat_province_row = list(typesObj.keys())
    heat_province_col = list(typesObj.values())
    # print(heat_province_row, heat_province_col)
    return heat_province_row, heat_province_col


if __name__ == '__main__':
    # get_scenic_count()
    # print(get_china_data())
    # print(get_price())
    # print(get_provien_scenic())
    # print(get_degreeLevel())
    # print(get_heat_data())
    print(get_scenic_stat())
