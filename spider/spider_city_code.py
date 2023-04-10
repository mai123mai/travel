import csv
import os
import time
from os.path import dirname, realpath

import requests

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
    "CNZZDATA1256662931": "1961980615-1678328734-https%253A%252F%252Freport.amap.com%252F%7C1680067642"
}
url = "https://report.amap.com/ajax/getCityInfo.do"

response = requests.get(url, headers=headers, cookies=cookies)
if response.status_code == 200:
    fieldnames = ['code', 'name', 'pinyin']
    if not os.path.exists('./city_code.csv'):
        with open('city_code.csv', 'w', newline='', encoding='utf-8') as csvfile:
            # 构造方法
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()  # 必须要调这个方法 才能写入首行
            writer.writerows(response.json())
    else:
        with open('city_code.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writerows(response.json())
else:
    print(response.status_code)


