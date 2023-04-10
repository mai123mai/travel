from util.getProvinceMap import get_province_map,get_city_name
from util.utils import *
from numpy import mean



def get_price_by_province():
    # 获取各省份景点的平均价格
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
    price_data = {}
    for i in set(typeList):
        prices = mean(list(map(lambda x: float(x), list(df_travel.loc[df_travel['address'].str.contains(i)]['price']))))
        mean_price = round(prices, 2)
        price_data[i] = mean_price
    xData = []
    yData1 = []  # 数量
    yData2 = []  # 价格
    for k, v in typesObj.items():
        xData.append(k)
        yData1.append(v)
        yData2.append(price_data.get(k))
    return xData, yData1, yData2


def getPriceDataByscenicName(searchName):
    province, map_url = get_province_map(searchName)
    city_names = get_city_name(map_url)
    citys = list(map(lambda x:x[:2], city_names))
    price_obj = []
    count_obj = []
    city_obj = []
    for i in citys:
        city_obj.append(i)
        sids = list(df_travel.loc[df_travel['address'].str.contains(i)]['sid'])
        price_list = []
        count = 0
        for sid in sids:
            price_text = float(list(df_travel[df_travel['sid'] == sid]['price'].values)[0])
            price_list.append(price_text)
            count += 1
        count_obj.append(count)
        if price_list:
            price = round(sum(price_list) / len(price_list), 2)
        else:
            price = 0
        price_obj.append(price)
    # print(city_obj)
    # print(count_obj)
    # print(price_obj)
    return city_obj, count_obj, price_obj


if __name__ == '__main__':
    # print(get_price_by_province())
    getPriceDataByscenicName('广东')