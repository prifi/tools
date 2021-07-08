#!/usr/bin/python
# -*- coding: utf-8 -*-
# 使用python2 commands模块

import re
import commands
import json

DROP_LIST = ['22','25']    # 排除端口

def filterList():
    DROP_str = ":" + "\\b|:".join(DROP_LIST) + '\\b'
    CMD="netstat -pntl | awk '{print $4,$7}'|grep  [0-9] |egrep -v '%s'" % (DROP_str)
    Result_Str = commands.getoutput(CMD)
    #print (Result_Str)
    tmp_list = Result_Str.split("\n") #每行加入列表
    new_dict = {}
    for line in tmp_list:
       #print (line)
       line_sub = re.sub(r':::|0.0.0.0:|::ffff:', '127.0.0.1:', line)
       #print (line_sub)
       PORT_REG = re.search(r"(\d+.\d+.\d+.\d+:)(\d+).+\d+/(\S+)",line_sub)
       if PORT_REG is not None:
           match_line =  (PORT_REG.groups())
           #new_dict[ match_line[-1]]  =  match_line[-2]
           new_dict[ match_line[-2] ]  =  (re.sub(r':','', match_line[-1]),re.sub(r':','', match_line[-3]))
    #print (new_dict)
    return new_dict

if __name__ == "__main__":
    Results = filterList()

    #格式化成适合zabbix lld的json数据
    ports = []
    for key  in  Results:
        ports += [{'{#PORT}':key,'{#NAME}':Results[key][0],'{#IP}':Results[key][1]}]
    #print (ports)
    #print json.dumps({'data':ports},sort_keys=True,indent=4,separators=(',',':'))
    jsonStr = json.dumps({'data':ports},sort_keys=True,indent=4)
    print jsonStr