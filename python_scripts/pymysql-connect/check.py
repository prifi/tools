#!/usr/bin/env python
#-*- coding:utf-8 -*-

import json, yaml
from pathlib import Path
from datetime import datetime, timedelta, timezone
from urllib.request import Request, urlopen

from connect import DB

basepath = Path(__file__).parent
ymlfile = basepath / 'config.yml'


class SqlCheck:
    """查询"""
    def __init__(self, site='xxx', interval=60):
        self.site = site
        self.interval = interval
        self.db = f'{self.site}-db'
        self.now = datetime.now()
        self.start = self.get_cstTime(self.now - timedelta(minutes=self.interval))
        self.end = self.get_cstTime(self.now)

        # 测试：2022-04-23 10:00:25 ~ 2022-04-23 11:00:25

        self.sql = f'select count(*) as total from {self.table} where add_time >= {int(self.start.timestamp())} \
                                and add_time <= {int(self.end.timestamp())}'


    def __getattr__(self, key):
        with ymlfile.open('rb') as f:
            self.locators = yaml.load(f, Loader=yaml.FullLoader)[self.__class__.__name__]
            if key in self.locators.keys():
                return self.locators.get(key)
        try:
            res = self.locators.get('mysql')[key]
            return res
        except:
            raise AttributeError(f'\'{self.__class__.__name__}\' object has no attribute \'{key}\'')

    # def test(self):
    #     print(self.host)
    #     print(self.site)

    def run(self, sql, fetchall=False):
        # 执行SQL
        with DB(host=self.host, port=self.port, db=self.db, user=self.user, passwd=self.passwd,) as db:
            db.execute(sql)
        return db.fetchall() if fetchall else db.fetchone()

    def get_cstTime(self, time):
        # 转换为CST时间
        if not time.tzinfo != 'UTC+08:00':
            return
        return time.astimezone(timezone(timedelta(hours=8)))

    def get_lowOrHigh(self, hour):
        # 获取低高峰期
        low = [i for i in range(13, 19)]
        return '低峰期' if hour in low else '高峰期'

    def get_data(self, title):
        # 构造企业微信发送通知
        data = {
            "msgtype": "markdown",
            "markdown": {
                "content": "<font color=\"comment\">{}</font>\n"
                           ">开始时间:<font color=\"comment\"> {:%Y-%m-%d %H:%M:%S}</font>\n"
                           ">结束时间:<font color=\"comment\"> {:%Y-%m-%d %H:%M:%S}</font>\n\n".format(title, self.start,
                                                                                                 self.end)
            }
        }
        return data

    def get_msg(self, title, text):
        # 构造订单异常发送的通知
        msg = self.get_data(title)
        msg["markdown"]["content"] += f"><font color=\"warning\">站点: **{text}**</font>\n"
        return msg

    def send_wechart(self, msg):
        # 发送企业微信通知
        req = Request(url=self.wechart_key, data=json.dumps(msg).encode(), method='POST')
        with urlopen(req) as response:
            response = response.read().decode()
            print(response)

    def main(self):
        res = self.run(sql=self.sql)
        return res

if __name__ == '__main__':
    SqlCheck().main()