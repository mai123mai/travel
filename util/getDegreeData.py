from util.utils import *


def get_commtent_level(searchName):
    df_travel['goodNum'] = df_travel['goodNum'].astype('int')
    df_travel['midNum'] = df_travel['midNum'].astype('int')
    df_travel['badNum'] = df_travel['badNum'].astype('int')
    if searchName == 'all':
        goodNum = sum(list(df_travel['goodNum']))
        midNum = sum(list(df_travel['midNum']))
        badNum = sum(list(df_travel['badNum']))
    else:
        goodNum = sum(list(df_travel.loc[df_travel['address'].str.contains(searchName)]['goodNum']))
        midNum = sum(list(df_travel.loc[df_travel['address'].str.contains(searchName)]['midNum']))
        badNum = sum(list(df_travel.loc[df_travel['address'].str.contains(searchName)]['badNum']))
    all_cnt = goodNum + midNum + badNum
    commtent_level_obj = [
        {
            "name": '好评',
            "value": goodNum,
        }, {
            "name": '中评',
            "value": midNum,
        }, {
            "name": '差评',
            "value": badNum,
        }
    ]
    # print(commtent_level_obj, all_cnt)
    return commtent_level_obj, all_cnt



if __name__ == '__main__':
    get_commtent_level('云南')
