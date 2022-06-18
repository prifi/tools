from webapp import app

if __name__ == '__main__':
    app.run('127.0.0.1', 8000, True)
    # 测试服务，不是部署的时候运行的，uwsgi guicorn
# xmlhttprequest 浏览器中用它发起get、post请求
# 当前网页不刷新
# 悄悄地背地里发出的request请求

