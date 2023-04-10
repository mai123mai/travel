from pymysql import *

conn = connect(
    host='127.0.0.1',
    user='root',
    password='123456',
    port=3306,
    database='dbm'
)
cursor = conn.cursor()


def querys(sql, params, type='no_select'):
    params = tuple(params)
    cursor.execute(sql, params)
    if type != 'no_select':
        data_list = cursor.fetchall()
        conn.commit()
        return data_list
    else:
        conn.commit()
        return '数据库语句执行成功'
