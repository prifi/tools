#!/usr/bin/env python
# -*- coding: utf-8 -*-

from webapp import app

if __name__ == '__main__':
    app.run('0.0.0.0', 8000, True)  # 启动服务，测试服务，部署使用uwsgi guicorn