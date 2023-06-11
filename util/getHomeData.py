from util.utils import *


def get_data_chart1():
    columns = list(df.columns)
    years = columns[2:][::-1]
    tourist = list(df[df['title'] == '国内游客(百万人次)'].values)[0][2:][::-1]
    tourist_towns = list(df[df['title'] == '城镇居民国内游客(百万人次)'].values)[0][2:][::-1]
    tourist_village = list(df[df['title'] == '农村居民国内游客(百万人次)'].values)[0][2:][::-1]
    dataList = []
    for y, i, j, k in zip(years, tourist, tourist_towns, tourist_village):
        dataList.append(
            {'name': y, '国内游客': i, '城镇居民游客': j, '农村居民游客': k}
        )
    cnt_pay = list(list(df.loc[df['title'] == '国内旅游总花费(亿元)'].values)[0][2:][::-1])
    towns_pay = list(list(df.loc[df['title'] == '城镇居民国内旅游总花费(亿元)'].values)[0][2:][::-1])
    village_pay = list(list(df.loc[df['title'] == '农村居民国内旅游总花费(亿元)'].values)[0][2:][::-1])
    speed_up = []
    for i in range(len(cnt_pay) - 1):
        speed_up.append(round(((cnt_pay[i + 1] - cnt_pay[i]) / cnt_pay[i]) * 100, 2))
    # print(speed_up)
    return dataList, years, cnt_pay, towns_pay, village_pay, speed_up


def get_data_chart2():
    columns = list(df.columns)
    years = columns[2:]
    # print(years)
    data_obj = []
    for year in years:
        village_cnt = list(df[year].values)[1]
        town_cnt = list(df[year].values)[2]
        data_list = [{'name': '城镇', 'value': village_cnt}, {'name': '农村', 'value': town_cnt}]
        # print(data_list)
        data_obj.append({
            "year": year,
            'data': data_list
        })
    # print(data_obj)
    return years, data_obj


def get_data_chart3():
    # columns = list(df.columns)
    # years = columns[5:][::-1]
    entry_visitors = list(df[df['title'] == '入境游客(万人次)'].values)[0][5:][::-1]
    entry_visitors_foreign = list(df[df['title'] == '外国人入境游客(万人次)'].values)[0][5:][::-1]
    entry_visitors_hk_macao = list(df[df['title'] == '港澳同胞入境游客(万人次)'].values)[0][5:][::-1]
    entry_visitors_taiwan = list(df[df['title'] == '台湾同胞入境游客(万人次)'].values)[0][5:][::-1]
    return list(entry_visitors), list(entry_visitors_foreign), list(entry_visitors_hk_macao), list(
        entry_visitors_taiwan)


def get_data_table():
    new_df = df.replace(0, np.nan)
    table_titles = new_df['title'].values
    # print(table_titles)
    table_years = list(new_df.columns[2:])
    # print(table_years)
    table_data = dict()
    for i in table_years:
        data = list(new_df[i].values)
        table_data[i] = data
    # print(table_data)
    return table_titles, table_years, table_data


if __name__ == '__main__':
    # dataList, years, cnt_pay, towns_pay, village_pay, speed_up = get_data_chart1()
    # print(cnt_pay,towns_pay, village_pay, speed_up)
    years, data_obj = get_data_chart2()
    print(years)
    # print(data_obj)
    print(get_data_chart3())
    # get_data_table()
