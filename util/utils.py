import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sqlalchemy import text


engine = create_engine('mysql+pymysql://root:123456@localhost/dbm')
con = engine.connect()
df = pd.read_sql(text('select * from china_tourism_data'), con=con)

df_travel = pd.read_sql(text('select * from travel'), con=con)
df_travel = df_travel.fillna(value='0')
df_travel.drop_duplicates(subset=['sid'], keep='first', inplace=True)
# df_comment = pd.read_sql(text('select * from comments'), con=con)

def get_traffic_df():
    df_1 = pd.read_sql(text('select * from traffic_congestion_index'), con=con)
    df_2 = pd.read_sql(text('select * from traffic_district_rank'), con=con)
    df_3 = pd.read_sql(text('select * from traffic_roadrank_rank'), con=con)
    return df_1,df_2,df_3

def typeList(seq, type, table='movie'):
    sql = f'select * from {table}'
    df = pd.read_sql(text(sql), con=con)
    type = df[type].values
    types = list(map(lambda x: x.split(seq), type))
    typeList = list()
    for i in types:
        for j in i:
            typeList.append(j)
    return typeList


if __name__ == '__main__':
    print(typeList('/', 'casts'))
