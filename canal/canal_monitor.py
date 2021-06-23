#!usr/bin/env python
# -*- coding:utf-8 -*-
# Dscribe: Monitor Canal consume log error.

import subprocess
import datetime
import re
import requests

def get_siteName():
    process = subprocess.Popen('hostname', stdout=subprocess.PIPE)
    stdout, stderr = process.communicate()
    hostname = stdout.decode()
    try:
        # usa-ali-komily-003
        siteNanme = re.search(r'usa-ali-(\S.+)-\w.+', hostname).groups()[0]
    except Exception as e:
        siteNanme = 'siteNameError'
    return siteNanme

def get_errorInfo():
    nowDate = datetime.datetime.now()
    nowSecond = (nowDate+datetime.timedelta(minutes=-1)).strftime("%Y-%m-%d %H:%M")
    canalErrorLog = "/data/service/canal-server/logs/{0}-db/{0}-db.log".format(get_siteName())
    process = subprocess.Popen(['grep -i \'{0}\' {1} | grep -i {2} |tail -1'.format(nowSecond, canalErrorLog, 'error')], shell=True, stdout=subprocess.PIPE)
    stdout, stderr = process.communicate()
    errorInfo = stdout.strip().decode()
    return errorInfo if errorInfo else None

def out_foramtStr(sitename, errorinfo):
    formatStr = '''**Canal同步异常** \n
        >**<font color=\"comment\">站点：{0}</font>**
        >**<font color=\"comment\">错误信息：</font>**`{1}`
        '''.format(sitename, errorinfo)
    data = {
        "msgtype": "markdown",
        "markdown": {
            "content": formatStr
        }
    }
    return data

if __name__ == '__main__':
    siteName = get_siteName()
    errorInfo = get_errorInfo()
    data = out_foramtStr(siteName, errorInfo)
    if errorInfo:
        robotUrl = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=9877effa-41fb-4855-910f-e20499e33937'
        requests.post(robotUrl, json=data)