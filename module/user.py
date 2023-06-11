from flask import request, render_template, session, redirect, Blueprint
import hashlib
from redis_cache import cache
from util import query

user = Blueprint('user', __name__)


# md5加密
def md5_string(in_str):
    md5 = hashlib.md5()
    md5.update(in_str.encode("utf8"))
    result = md5.hexdigest()
    return result

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
            return request.form['email'] in item and md5_string(request.form['password']) in item
        users = query.querys('select * from user', [], 'select')
        filter_users = list(filter(filter_fl, users))
        if len(filter_users):
            """设置session的数据 login设置"""
            email = request.form['email']
            session['email'] = email
            names = maps(query.querys("SELECT name FROM USER WHERE email=%s", [email], 'select'))[0]
            session['name'] = names
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
        md5_pwd = md5_string(password)
        pwd = maps(query.querys("SELECT password FROM USER WHERE email=%s", [email], 'select'))[0]
        if md5_pwd == pwd:
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
            return render_template('erro.html', message='User has registered', back='/register')
        else:
            password = request.form.get('password')
            pwd = md5_string(password)
            query.querys('insert into user(name,email,password) value(%s,%s,%s)',
                         [request.form.get('name'), request.form.get('email'),pwd])
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
                passwordChecked = request.form['passwordChecked']
                if password == passwordChecked:
                    email = request.form['email']
                    query.querys('UPDATE `USER` SET password = %s  WHERE email= %s ;', [md5_string(password), email])
                    return redirect('/login')
                else:
                    return render_template('erro.html', message='User not registered', back='/forget')
            else:
                return render_template('erro.html', message='Password inconsistency', back='/forget')
