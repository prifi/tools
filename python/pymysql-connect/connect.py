#!/usr/bin/env python
#-*- coding:utf-8 -*-

import pymysql

class DB:
    """mysql连接"""
    def __init__(self, host, port, db, user, passwd, charset='utf8'):
        # 建立连接
        self.conn = pymysql.connect(host=host, port=port, db=db, user=user, passwd=passwd, charset=charset)
        self.cur = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    def __enter__(self):
        # 返回游标
        return self.cur

    def __exit__(self, exc_type, exc_val, exc_tb):
        # 执行并关闭连接
        self.conn.commit()
        self.cur.close()
        self.conn.close()