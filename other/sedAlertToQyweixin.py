#!/usr/bin/env python
#coding=utf-8
'''
    Suprevisord Listener example.
'''
import requests
import sys
import os
import socket

msg = 'test'

# baojing
hostname = socket.gethostname()
robotUrl = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send..'

formatStr = '''【告警】<font color=\"warning\">`{0}`</font> \n
    ><font color=\"comment\">当前主机: {1}</font>'''.format(msg, hostname)

data = {
    "msgtype": "markdown",
    "markdown": {
        "content": formatStr
    }
}
requests.post(robotUrl, data=json.dumps(data))