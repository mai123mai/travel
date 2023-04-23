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




