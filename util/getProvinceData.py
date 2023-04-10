from util.utils import *


def get_province_bytype(type):
    # 根据省份获取景点数和人流量
    sids = list(df_travel.loc[df_travel['address'].str.contains(type)]['sid'])
    scenic_cnt = len(sids)
    totalNum_list = list(map(lambda x: int(x) if x else 0,df_travel.loc[df_travel['address'].str.contains(type)]['totalNum']))
    totalNum = sum(totalNum_list)
    return scenic_cnt, totalNum



if __name__ == '__main__':
    print(get_province_bytype('云南'))

