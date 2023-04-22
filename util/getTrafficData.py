import json

import requests

from util.utils import get_traffic_df

df_1, df_2, df_3,df_4 = get_traffic_df()


def get_traffic_index(searchName):
    new_df = df_1[df_1['name'].str.contains(searchName)][['data', 'typyid']]
    data = new_df['data'].tolist()
    if data:
        data1 = eval(data[0])
        data2 = eval(data[1])
        data3 = eval(data[2])
        data4 = eval(data[3])
    else:
        return ''
    # print(data)
    row_data1 = [i[0].split(' ')[-1] for i in data1]
    col_data1 = [i[1] for i in data1]
    row_data2 = [i[0].split(' ')[-1] for i in data2]
    col_data2 = [i[1] for i in data2]
    row_data3 = [i[0].split(' ')[-1] for i in data3]
    col_data3 = [i[1] for i in data3]
    row_data4 = [i[0].split(' ')[-1] for i in data4]
    col_data4 = [i[1] for i in data4]

    return row_data1, col_data1, row_data2, col_data2, row_data3, col_data3, row_data4, col_data4


def get_traffic_district_data(searchName):
    new_df = df_2[df_2['name'].str.contains(searchName)][['data', 'typyid']]
    datas = new_df['data'].tolist()
    item_obj = []
    for data in datas:
        item = json.loads(data)
        item_obj.append(item)
    return item_obj


def get_traffic_roadrank_data(searchName):
    new_df = df_3[df_3['name'].str.contains(searchName)][['data', 'typyid']]
    datas = new_df['data'].tolist()
    roadrank_item_obj = []
    for data in datas:
        item = json.loads(data)
        roadrank_item_obj.append(item)
    return roadrank_item_obj


def get_map_data(searchName):
    new_df = df_4[df_4['name'].str.contains(searchName)][['data', 'center']]
    datas = new_df['data'].tolist()[0]
    center_str = new_df['center'].tolist()[0]
    mapdata = json.loads(datas)
    center = json.loads(center_str)
    return mapdata, center


if __name__ == '__main__':
    # print(get_traffic_index('广州'))
    # print(get_traffic_district_data('广州'))
    print(get_map_data('广州'))

