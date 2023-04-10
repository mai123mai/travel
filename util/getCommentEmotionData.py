from emotion.emotion_train import *

import os

path = os.path.dirname(os.path.dirname(__file__))


def get_comment_score_data(searchName):
    sql = f'select sid from travel WHERE title like "%{searchName}%" limit 5000'
    sid_pd = pd.read_sql(text(sql), con=con)
    if sid_pd.empty:
        return [], '', ''
    sid = sid_pd['sid'].tolist()[0]
    posImg_src, negImg_src, score_src = start_emotion_train(sid)
    emotional_score = pd.read_csv(score_src)
    score_time_list = emotional_score[['content_time', 'amend_weight']].values.tolist()
    typesObj = {}
    for t, v in score_time_list:
        if typesObj.get(t, -1) == -1:
            typesObj[t] = [v]
        else:
            typesObj[t].append(v)
    sort_list = sorted(typesObj.items(), key=lambda x: x[0], reverse=False)
    ydata = []
    for i in sort_list:
        mid = round(sum(i[1]) / len(i[1]), 1)
        ydata.append([i[0], mid])
    return ydata, posImg_src, negImg_src,


if __name__ == '__main__':
    print(get_comment_score_data('紫微洞'))

