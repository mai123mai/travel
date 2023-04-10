# coding=utf-8
import json

from flask import Flask, request, render_template, session, redirect, jsonify
from flask_sqlalchemy import Pagination

from travel.module.dataShow import dataShow
from travel.module.user import user
from travel.module.dataAnaly import dataAnaly
from travel.emotion.emotion_train import *
from travel.redis_cache import cache
from travel.util.getTableData import getTableDataBYTablePage
from travel.util.query import querys

app = Flask(__name__)
cache.init_app(app)
app.secret_key = 'This is session_key you know ?'

urls = [user, dataShow, dataAnaly]
for url in urls:
    app.register_blueprint(url)  # 将三个路由均实现蓝图注册到主app应用上


@app.route('/')
def allRequest():
    return redirect('/login')


@app.before_request
def before_request():
    pat = re.compile(r'^/static')
    if re.search(pat, request.path):
        return
    if request.path == '/login':
        return
    if request.path == '/register':
        return
    if request.path == '/forget':
        return
    if request.path == '/loginOut':
        return
    email = session.get('email')
    if email:
        return None
    return redirect('/login')




@app.after_request
def cors(environ):
    environ.headers['Access-Control-Allow-Origin'] = '*'
    environ.headers['Access-Control-Allow-Method'] = '*'
    environ.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return environ






if __name__ == '__main__':
    app.run(debug=True, port=8888)
