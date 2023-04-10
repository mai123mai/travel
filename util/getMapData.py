import random

from util.getProvinceMap import get_city_heat_sort
from util.utils import *
from numpy import mean


def get_map_data_chart1(searchName):
    if searchName == 'all':
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
        # print(typesObj)
        city_names = list(typesObj.keys())
        scenic_cnts = list(typesObj.values())
    else:
        city_names, scenic_cnts = get_city_heat_sort(searchName)
    change_data, city_name_list = create_change(city_names,scenic_cnts)
    return change_data, city_name_list


def create_change(city_names, scenic_cnts):
    new_total_num_obj = {}
    for total, city in zip(scenic_cnts, city_names):
        j = 0
        new_total_num = []
        for i in range(10):
            r = random.randint(total // 12, total // 10)
            j += r
            new_total_num.append(j)
        new_total_num.append(total)
        new_total_num.sort(reverse=True)
        new_total_num_obj[city] = new_total_num
    data_list = sorted(new_total_num_obj.items(), key=lambda x: x[1][-1], reverse=True)
    change_data = []
    for i in range(11):
        temp = []
        for j in data_list:
            temp.append(j[1][i])
        # print(temp)
        change_data.append(temp)
    # print(change_data)
    city_name_list = [i[0] for i in data_list]
    return change_data, city_name_list


if __name__ == '__main__':
    print(get_map_data_chart1('广东'))
