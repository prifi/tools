#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, jsonify, request, Response, Request

app = Flask('cmdb')


# / => function 映射
@app.route('/')
def index():
    # return 'Hello Flask!'
    return """
    <html>
    <head> 
    <title>首页</title>
    </head>
    <body>
        <h1>Hello FLask!</h1>
    </body>
    </html>
    """


# 渲染模板
@app.route('/t')
def get_html():
    return render_template('index.html')


# 返回json
@app.route('/j', methods=['GET'])
def get_json():
    d = {'a': 1, 'b': 2, 'ad': ['a', 'b']}
    return jsonify(d)


# ------------- login demo -------------

# 登录
@app.route('/login')
def login():
    return render_template('login.html')


def get_user(username):
    # 数据库查询用户，返回密文密码
    return '123'


def encrypt(password):
    # 加密算法，加密提交上来的密码
    return '123'


#  用户认证逻辑
@app.route('/auth', methods=['POST'])
def auth():
    try:
        username = request.form['username']
        password = request.form['password']
        # 数据库查询用户，验证比对密码逻辑
        pwd = get_user(username)
        if encrypt(password) == pwd:
            return jsonify({
                'meta': {'code': 0},
                'user': {'id': 100, 'username': username}  # 成功
            })
    except:
        pass
    return jsonify({
        'meta': {'code': 1, 'msg': '用户名或密码错误'}  # 失败
    })
