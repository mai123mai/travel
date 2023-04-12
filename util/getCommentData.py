from util.utils import *




def get_comment_t_top10():
    df2 = df_travel
    df2.drop_duplicates(subset=['sid'], keep='first', inplace=True)
    df2['totalNum'] = df2['totalNum'].astype(int)
    df2 = df2.sort_values(by='totalNum', ascending=False)
    sid_top10 = list(df2['sid'].values[:10])
    sid_top1 = sid_top10[0]
    title_top10 = list(df2['title'].values[:10])
    data_obj = {}
    for s, t in zip(sid_top10, title_top10):
        data_obj[t] = s
    return data_obj, sid_top1


def get_echart1_data(sid):
    engine = create_engine('mysql+pymysql://root:123456@localhost/dbm')
    con = engine.connect()
    df_comment = pd.read_sql(text(f'select comment_time from comments where `sid` = {sid}'), con=con)
    comment_time = list(df_comment['comment_time'].values)
    typesObj = {}
    for i in comment_time:
        if typesObj.get(i, -1) == -1:
            typesObj[i] = 1
        else:
            typesObj[i] += 1
    # print(typesObj)
    sort_list = sorted(typesObj.items(), key=lambda x: x[0], reverse=False)
    ydata = [list(i) for i in sort_list]
    return ydata


if __name__ == '__main__':
    s = get_echart1_data(1394)
    print(s)
