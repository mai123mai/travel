from util.getProvinceMap import get_province_map, get_city_name
from util.utils import *


def get_all_province():
    addressList = df_travel['address'].values
    types = list(map(lambda x: x.split(','), addressList))
    typeList = set()
    for i in types:
        typeList.add(i[0])
    return list(typeList)


def get_star_by_province(searchName):

    if searchName == 'all':
        star_list = df_travel['starNum'].values
    else:
        sids = list(df_travel[df_travel['address'].str.contains(searchName)]['sid'].values)
        star_list = []
        for sid in sids:
            s = list(df_travel.loc[df_travel['sid'] == sid]['starNum'].values)
            if not s:
                continue
            else:
                s = float(s[0])
            star_list.append(s)
    starObj = {}
    star_list.sort()
    # print(rateList)
    for i in star_list:
        if starObj.get(i, -1) == -1:
            starObj[i] = 1
        else:
            starObj[i] += 1
    return list(starObj.keys()), list(starObj.values())


def getStarDataByscenicName(searchName):
    province, map_url = get_province_map(searchName)
    city_names = get_city_name(map_url)
    citys = list(map(lambda x: x[:2], city_names))
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
    print(get_star_by_province('广东'))
