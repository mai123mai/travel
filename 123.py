from flask_sqlalchemy import Pagination


def select():
    pagination = Pagination(page=1, per_page=10)
    print('items 当前页面的所有记录:', pagination.items)
    print('page 当前页码:', pagination.page)
    print('per_page 每页显示记录条数:', pagination.per_page)
    print('has_prev 是否有上一页:', pagination.has_prev)
    print('prev_num 上一页页码:', pagination.prev_num)
    print('has_next 是否有下一页:', pagination.has_next)
    print('next_num 下一页页码:', pagination.next_num)
    print('pages 查询得到的总页数:', pagination.pages)
    print('total 总记录条数:', pagination.total)


if __name__ == '__main__':
    select()