from flask import request, render_template, session, redirect, Blueprint

from redis_cache import cache
from util import query

user = Blueprint('user', __name__)


@user.route('/loginOut')
def loginOut():  # put application's code here
    session.clear()
    cache.clear()
    return render_template('logout.html')


@user.route('/login', methods=['GET', 'POST'])
def login():  # put application's code here
    maps = lambda x: x[0] if x else ''
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        request.form = dict(request.form)

        # print(request.form)

        def filter_fl(item):
            return request.form['email'] in item and request.form['password'] in item

        users = query.querys('select * from user', [], 'select')
        filter_users = list(filter(filter_fl, users))
        """设置session的数据 login设置"""
        email = request.form['email']
        session['email'] = email
        names = maps(query.querys("SELECT name FROM USER WHERE email=%s", [email], 'select'))[0]
        session['name'] = names
        if len(filter_users):
            return redirect('/home')
        else:
            return render_template('erro.html', message="The email address or password is incorrect",
                                   back='./login')


@user.route('/lock_screen', methods=['GET', 'POST'])
def lock_screen():
    maps = lambda x: x[0] if x else ''
    email = session.get('email')
    names = maps(query.querys("SELECT name FROM USER WHERE email=%s", [email], 'select'))[0]
    if request.method == 'GET':
        return render_template('lock_screen.html', name=names)
    elif request.method == 'POST':
        request.form = dict(request.form)
        password = request.form['password']
        pwd = maps(query.querys("SELECT password FROM USER WHERE email=%s", [email], 'select'))[0]
        if password == pwd:
            return redirect('/home')
        else:
            return render_template('erro.html', message='密码不对', back='/lock_screen')


@user.route('/register', methods=['GET', 'POST'])
def register():  # put application's code here
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        request.form = dict(request.form)

        def filter_fl(item):
            '''
            判断是否已经注册
            :param item:
            :return:
            '''
            return request.form['email'] in item

        users = query.querys('select * from user', [], 'select')
        filter_list = list(filter(filter_fl, users))
        if len(filter_list):
            return render_template('erro.html', message='User not registered', back='/register')
        else:
            query.querys('insert into user(name,email,password) value(%s,%s,%s)',
                         [request.form.get('name'), request.form.get('email'), request.form.get('password')])
            return redirect('/login')


@user.route('/forget', methods=['GET', 'POST'])
def forget():  # put application's code here
    if request.method == 'GET':
        return render_template('recoverpw.html')
    elif request.method == 'POST':
        request.form = dict(request.form)
        if request.form['password'] != request.form['passwordChecked']:
            return render_template('erro.html', message='Password inconsistency', back='/forget')
        else:
            def filter_fl(item):
                '''
                判断是否已经注册
                :param item:
                :return:
                '''
                return request.form['email'] in item

            users = query.querys('select * from user', [], 'select')
            filter_list = list(filter(filter_fl, users))
            if len(filter_list):
                password = request.form['password']
                email = request.form['email']
                query.querys('UPDATE `USER` SET password = %s  WHERE email= %s ;', [password, email])
                return redirect('/login')
            else:
                return render_template('erro.html', message='User not registered', back='/forget')
