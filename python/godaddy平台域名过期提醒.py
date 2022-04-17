#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@version:
author:fly
@time: 2022/04/12
@file: Godaddy平台域名过期提醒.py
@function:
@modify:
"""
#!usr/bin/env python
# -*- coding:utf-8 -*-
# Godaddy域名过期30天分别提醒发送企业微信通知
# Godaddy Api 使用获取域名列表，更多API参考：https://developer.godaddy.com/doc
# curl -X GET -H "Authorization: sso-key key:secret" "https://api.godaddy.com/v1/domains"

import json, re
from urllib.request import Request, urlopen
from urllib.error import URLError
from datetime import datetime

class Godaddy:

    def __init__(self, day=30, url="https://api.godaddy.com/v1/domains"):
        self.api_url = url
        self.expireDay = day
        self._key = "xxx"
        self._secret = "xxx"
        self._wechart_key = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx'

    def get_headers(self):
        '添加认证header头'
        headers = {
            "Accecpt": "application/json",
            "Content-Type": "application/json",
            "Authorization": "sso-key {}:{}".format(self._key, self._secret)
        }
        return headers

    def get_expiresDomainList(self):
        '获取即将过期域名列表'
        req = Request(url=self.api_url, headers=self.get_headers())
        try:
            with urlopen(req) as f:
                dj = f.read().decode('utf-8')
        except URLError as e:
            if hasattr(e, 'reason'):
                print('Reason: ', e.reason)
            elif hasattr(e, 'code'):
                print('Error code: ', e.code)
        else:
            dp = json.loads(dj)
            dl = [ {
                    'domainName': i['domain'],
                    'expireTime': i['expires'].split('T')[0],
                    'endDays': self.get_expireDay(i['expires'], self.expireDay)
                    }
                   for i in dp if i['status'] == 'ACTIVE'
                   and self.get_expireDay(i['expires'], self.expireDay)
            ]
            return sorted(dl, key=lambda d: d['endDays'])

    def get_expireDay(self, ts, d, ed=datetime.today()):
        '获取即将过期天数'
        ss = re.match(r'(\S+)T.*', ts).group(1)
        sd = datetime.strptime(ss, "%Y-%m-%d")
        cd = (sd - ed).days
        return cd if cd <= d else None

    def _alert_message(self, domains):
        '构造告警信息'
        data = {
            "msgtype": "markdown",
            "markdown": {
                "content": "<font color=\"warning\">Godaddy 域名即将过期，请相关同事注意。</font>\n"
            }
        }
        for domain in domains:
            s = '><font color=\"comment\">域名: {domainName}  到期时间: {expireTime}  剩余天数: {endDays}</font> \n'.format(**domain)
            data["markdown"]["content"] += s
        # print(data)
        return data

    def send_wechart(self, domains):
        '发送企业微信通知'
        req = Request(url=self._wechart_key, data=json.dumps(self._alert_message(domains)).encode(), method='POST')
        with urlopen(req) as response:
            response = response.read().decode()
            # print(response)

    def main(self):
        domains = self.get_expiresDomainList()
        if domains:
            self.send_wechart(domains)

if __name__ == '__main__':
    Godaddy().main()