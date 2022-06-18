#!/usr/bin/python
# coding: UTF-8
import StringIO  
import pycurl  
import sys  
import os  
import json

# 将要监控的web站点url添加到列表
file = '/etc/zabbix/web_speed.txt'
#www.baidu.com

class Http_Test:  
    def __init__(self):
        self.contents = ''
    def body_callback(self,buf):
        self.contents = self.contents + buf

def Get_Urllist():
    urllist = []
    with open(file) as f:
        for i in f.readlines():
            if i[0] != '#':
                urllist.append(i.strip('\n'))
    u = []
    for i in urllist:
        u += [{'{#URL}': i}]
    print json.dumps({'data':u},sort_keys=True,indent=4)

#def Format_Str():
#    s = [ "connec_time","namelookup_time","total_time","pretransfer_time","starttransfer_time" ]
#    p = []
#    for i in s:
#        p += [{'{#STATUS}': i}]
#    print json.dumps({'data':p},sort_keys=True,indent=4)
    
        
def Check_Url(url):  
    t = Http_Test()
    c = pycurl.Curl()
    c.setopt(pycurl.WRITEFUNCTION,t.body_callback)
    c.setopt(pycurl.ENCODING, 'gzip')
    c.setopt(pycurl.URL,url)
    c.perform()
    s = {}
#     s['http_code'] = c.getinfo(pycurl.HTTP_CODE)
    s['connect_time'] = c.getinfo(pycurl.CONNECT_TIME)
    s['namelookup_time'] = c.getinfo(pycurl.NAMELOOKUP_TIME)
    s['total_time'] = c.getinfo(pycurl.TOTAL_TIME)
    s['pretransfer_time'] = c.getinfo(pycurl.PRETRANSFER_TIME)
    s['starttransfer_time'] = c.getinfo(pycurl.STARTTRANSFER_TIME)
    return s

if __name__ == "__main__":
    try:
        if sys.argv[1] == "web_speed_discovery":
            #Format_Str()
            Get_Urllist()
        elif sys.argv[1] == "web_speed_list":
            print("%.3f" % (Check_Url(sys.argv[2])[sys.argv[3]]))
        else:
            print("Pls sys.argv[0] web_speed_discovery | web_speed_list[{#URL},{#STATUS}] ")
    except Exception as msg:
        print(msg)