import json
import time
import pandas as pd
import pymysql
from datetime import datetime
import requests


# print(pd_codes)
def conn_myqsl():
    db = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='dbm')
    cursor = db.cursor()  # 游标
    return db, cursor


def save_data(table_name, data):
    # 列表  1个列表 一条数据
    db, cursor = conn_myqsl()
    params = ','.join(['%s'] * len(data))
    try:
        sql = f'replace into {table_name} values ({params})'
        cursor.execute(sql, tuple(data))
        db.commit()
        print(data)
    except Exception as e:
        print('erro---->' + str(e))
        db.rollback()


def get_traffic_index(code, name, dataType):
    headers = {
        "authority": "report.amap.com",
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "referer": "https://report.amap.com/detail.do?city=110000",
        "sec-ch-ua": "\"Google Chrome\";v=\"111\", \"Not(A:Brand\";v=\"8\", \"Chromium\";v=\"111\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"macOS\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
        "x-requested-with": "XMLHttpRequest"
    }
    cookies = {
        "UM_distinctid": "186c4403e38c6a-0a3bdde65878a-1f525634-13c680-186c4403e391164",
        "cna": "+I7mGwN/qg0CAXeT1UkgDPIu",
        "isg": "BCUlEPISrTyYV8lgnDcXzT2jNOdfYtn0hXxYLCcK9txoPkWw77bxxLHfzKJIPvGs",
        "l": "fBa6Q9QgNNEsl7EYBOfZPurza779bIRAguPzaNbMi9fPO6fBsNKAW1MtnvL6CnGVFsZeR3JGlUzkBeYBc3K-nxvtgC4K1AkmnmOk-Wf..",
        "tfstk": "cNlPBdOidWmb1EupXSVEQKgXTQuRZOli9izQEHONtMVlV82liMILoJFU3R_Vx8f..",
        "user_unique_id": "a187bf65864ea91c01872bfd30b61830",
        "SESSION": "79566f6d-7438-4300-b9cd-bbe6feeca5ed",
        "CNZZDATA1256662931": "1961980615-1678328734-https%253A%252F%252Freport.amap.com%252F%7C1680074937"
    }
    url = "https://report.amap.com/ajax/cityHourly.do"
    params = {
        "cityCode": code,
        "dataType": dataType
    }

    response = requests.get(url, headers=headers, cookies=cookies, params=params)
    datas = response.json()
    # print(datas)
    for data in datas:
        timeStap = data[0] * 0.001
        local_time = time.localtime(timeStap)
        t = time.strftime("%Y-%m-%d %H:%M", local_time)
        data[0] = t
    datas = json.dumps(datas)
    times = datetime.now().strftime('%Y-%m-%d %H:%M')
    id = str(code) + '_' + str(dataType)
    table_name = 'traffic_congestion_index'
    save_data(table_name, [id, times, code, name, dataType, datas])


def get_districtRank_data(code, cityname, dataType):
    headers = {
        "authority": "report.amap.com",
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "referer": "https://report.amap.com/detail.do?city=440100",
        "sec-ch-ua": "^\\^.Not/A)Brand^^;v=^\\^99^^, ^\\^Google",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "^\\^Windows^^",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
        "x-requested-with": "XMLHttpRequest"
    }
    cookies = {
        "user_unique_id": "a185bbc7864ea8e701872db043f30aac",
        "SESSION": "3ca1e5d4-2494-4f2c-8dd8-1379ec2e2f99",
        "UM_distinctid": "1872db04825279-0909f1aed02481-26021a51-1fa400-1872db048268e1",
        "CNZZDATA1256662931": "305016805-1680096682-https^%^253A^%^252F^%^252Freport.amap.com^%^252F^%^7C1680096682"
    }
    url = "https://report.amap.com/ajax/districtRank.do"
    params = {
        "linksType": dataType,
        "cityCode": code
    }
    response = requests.get(url, headers=headers, cookies=cookies, params=params)

    json_datas = response.json()
    items = []
    for item in json_datas:
        pid = item.get('id')
        number = item.get('number')
        name = item.get('name')
        index = item.get('index')
        speed = item.get('speed')
        items.append([pid, number, name, index, speed])
    datas = json.dumps(items)
    id = str(code) + '_' + str(dataType)
    times = datetime.now().strftime('%Y-%m-%d %H:%M')
    table_name = 'traffic_district_rank'
    save_data(table_name, [id, times, code, cityname, dataType, datas])


def get_roadRank_data(code, cityname, dataType):
    headers = {
        "authority": "report.amap.com",
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "referer": "https://report.amap.com/detail.do?city=440100",
        "sec-ch-ua": "\".Not/A)Brand\";v=\"99\", \"Google Chrome\";v=\"103\", \"Chromium\";v=\"103\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
        "x-requested-with": "XMLHttpRequest"
    }
    cookies = {
        "user_unique_id": "a185bbc7864ea8e701872db043f30aac",
        "SESSION": "3ca1e5d4-2494-4f2c-8dd8-1379ec2e2f99",
        "UM_distinctid": "1872db04825279-0909f1aed02481-26021a51-1fa400-1872db048268e1",
        "CNZZDATA1256662931": "305016805-1680096682-https%253A%252F%252Freport.amap.com%252F%7C1680100307"
    }
    url = "https://report.amap.com/ajax/roadRank.do"
    params = {
        "roadType": dataType,
        "timeType": "0",
        "cityCode": code,
    }
    response = requests.get(url, headers=headers, cookies=cookies, params=params)
    json_datas = response.json().get('tableData')
    items = []
    for item in json_datas:
        number = item.get('number')
        name = item.get('name')
        dir = item.get('dir')
        index = item.get('index')
        speed = item.get('speed')
        travelTime = item.get('travelTime')
        delayTime = item.get('delayTime')
        items.append([number, name, dir, index, speed, travelTime, delayTime])
    datas = json.dumps(items)
    id = str(code) + '_' + str(dataType)
    times = datetime.now().strftime('%Y-%m-%d %H:%M')
    table_name = 'traffic_roadrank_rank'
    save_data(table_name, [id, times, code, cityname, dataType, datas])


def run():
    pd_city = pd.read_csv('city_code.csv')
    # print(pd_codes)
    pd_codes = pd_city[['code', 'name']].values.tolist()
    for i in pd_codes:
        for typeindex in range(1, 5):
            get_traffic_index(i[0], i[1], typeindex)
        for typeindex_1 in [1, 3, 4]:
            get_districtRank_data(i[0], i[1], typeindex_1)
        for typeindex_2 in [0, 1, 2]:
            get_roadRank_data(i[0], i[1], typeindex_2)


if __name__ == '__main__':
    run()

# print(dirname(realpath(__file__)))
