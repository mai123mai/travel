import random
from urllib.parse import urlencode

from redis import Redis
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import text

sr = Redis(host='127.0.0.1', port=6379, db=1)
engine = create_engine('mysql+pymysql://root:dgut0213@localhost/dbm')
con = engine.connect()
url = "https://www.ly.com/scenery/AjaxHelper/DianPingAjax.aspx"
df = pd.read_sql(text('select distinct(sid) from travel where totalNum != 0;'), con=con)
sids = list(df['sid'].values)
# print(sids)
for sid in sids:
    params = {
        "action": "GetDianPingList",
        "sid": str(sid),
        "page": '1',
        "pageSize": "10",
        "labId": "6",
        "sort": "0",
        "iid": random.random()
    }
    href = url + "?" + urlencode(params)
    result = sr.rpush('comment_url', href)


# 获取
# li = sr.lrange('comment_url', 0, 5)
# print(li)
# for i in li:
#     print(i.decode())
#
# import redis
# conn = redis.Redis('127.0.0.1',db=1)
# url = 'https://www.ly.com/scenery/AjaxHelper/DianPingAjax.aspx?action=GetDianPingList&sid=111&page=1&pageSize=10&labId=1&sort=0&iid=0.3952226431943444'
# sr.lpush('comment_url',url)

