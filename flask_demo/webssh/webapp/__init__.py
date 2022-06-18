from flask import Flask, render_template, jsonify, request, Response, Request
import re
from tools.ssh import SSHClient
from uuid import uuid4

app = Flask('webssh')
pattern = '(?P<host>[\d.]+)[,\s]+(?P<username>[a-zA-Z0-9_-]+)[,\s]+(?P<password>\w+)[,\s]+(?P<port>\d+)' # 字符的集合，元字符，表示1个字符
regex = re.compile(pattern)

# server asp jsp php request.url -> function
# / function 的映射
@app.route('/')
def index():
    # info = '{}<br>{}<br>{}<br>'.format(
    #     app.template_folder, # 默认模板路径
    #     app.static_folder,   # 默认静态物理路径
    #     app.static_url_path  # 默认逻辑路径，http://www.magedu.com/static/js/xx.js
    # )
    return render_template('index.html')

ssh_clients = {} # redis memcached str bytes

@app.route('/ssh')
def sshconn():
    try:
        qs = request.args
        print(qs, '~~~~~')
        connstr = qs.get('connstr', '').strip()
        m = regex.match(connstr)
        if m:
            # m.groupdict{'host': '192.168.142.140', 'username': 'python', 'password': 'python', 'port': '22'}
            client = SSHClient(**m.groupdict()) # session
            uid = uuid4().hex # 16 # cookie

            response:Response = jsonify({
                'meta':{'code':0},
                'data':''
            })
            response.set_cookie('uid', uid) # response 报文的set-cookie
            ssh_clients[uid] = client
            return response
    except Exception as e:
        pass # 记录日志
    return jsonify({'meta':{'code':100, 'msg':'连接失败，找管理员去，别找我'}})

@app.route('/ssh/<cmd>') # urlencode
def excute(cmd:str):
    # 怎么执行？client
    try:
        uid = request.cookies.get('uid', '')
        client:SSHClient = ssh_clients.get(uid, None)
        if client:
            stdin, stdout, stderr = client.exec(cmd)
            output1 = stdout.read().decode()  # utf-8
            output2 = stderr.read().decode()

            return {
                'meta': {'code': 0},
                'data': {
                    'output':"{}<br>{}".format(output1, output2)
                }
            }
    except Exception as e:
        pass # 记录错误
    # 找不到呢
    return jsonify({'meta':{'code':300, 'msg':'您的连接有错误，请重新连接'}})

# @app.route('/login')
# def get_html():
#     return render_template('login.html')

# @app.route('/auth', methods=['POST', 'OPTIONS'])
# def auth(): # 用户认证，只认POST
#     try:
#         username = request.form['username']
#         password = request.form['password']
#         pwd = get_mysql(username)
#         print('=' * 30)
#         if encrypt(password) == pwd:
#             # 去数据库查询用户名，查到该用户了，拿出密码，使用密码函数加密
#             res:Response = jsonify({
#                 'meta':{'code':0},
#                 'user':{'id':100, 'uername':username}
#             })
#             # res.headers.set('Access-Control-Allow-Origin', '*')
#             # res.headers.set('Access-Control-Allow-Methods', '*')
#             # print(res.headers)
#             return res
#     except:
#         pass
#     return jsonify({
#         'meta':{'code':1, 'msg':'用户名或密码错误'}
#     })
#
# @app.route('/j', methods=['GET'])
# def get_json():
#     d = {'a':1, 'b':'abc', 'c':[1, 'ad', ['a', 'b']]}
#     return jsonify(d)

# 前后端分离的时候，后端就成了数据源，不提供网页
