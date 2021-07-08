#!/usr/bin/env python
# coding:utf-8
# @监控站点响应码及证书过期

import os, sys, json

# 将要监控的web站点url添加到urllist列表
files_1='/etc/zabbix/moniter_web.txt'  #SITENAME|URL
files_2='/etc/zabbix/check_cert.txt'   #SITENAME|IP

# 这个函数主要是构造出一个特定格式的字典，用于zabbix
def web_site_discovery(file_name):
    urllist = []
    with open(file_name) as f:
        for i in f.readlines():
            if i[0] != '#':
                urllist.append(i.strip('\n'))

    web_list = []
    web_dict = {"data": None}

    for url in urllist:
        url_dict = {}
        url_dict["{#SITENAME}"] = url.split('|')[0]
        url_dict["{#URL}"] = url.split('|')[1]
        web_list.append(url_dict)

    web_dict["data"] = web_list
    jsonStr = json.dumps(web_dict, sort_keys=True, indent=4)
    return jsonStr

# 这个函数用于测试站点返回的状态码，注意在cmd命令中如果有%{}这种字符要使用占位符代替，否则会报错
def web_site_code():
    cmd = 'curl --connect-timeout 10 -m 20 -o /dev/null -s -w %s %s' % ("%{http_code}", sys.argv[2])
    reply_code = os.popen(cmd).readlines()[0]
    return reply_code

# 检测站点证书是否过期
def web_check_expire():
    cmd1 = 'echo | timeout 6 openssl s_client -servername %s -connect %s:443 2>/dev/null | openssl x509 -noout -dates | grep notAfter | awk -F "=" \'{print $NF}\'' % (sys.argv[2], sys.argv[3])
    end_date_time = os.popen(cmd1).readlines()[0].strip()

    cmd2 = 'date %s --date "%s"' % ('\'+%s\'',end_date_time)
    end_data_seconds = os.popen(cmd2).readlines()[0].strip()

    cmd3 = 'date \'%s\'' % '+%s'
    now_seconds = os.popen(cmd3).readlines()[0].strip()

    cmd4 = 'echo "(%s-%s)/24/3600" | bc' % (end_data_seconds,now_seconds)
    expire_time = os.popen(cmd4).readlines()[0].strip()

    return expire_time

if __name__ == "__main__":
    try:
        if sys.argv[1] == "web_site_discovery":
            print(web_site_discovery(files_1))
        elif sys.argv[1] == "web_check_cert":
            print(web_site_discovery(files_2))
        elif sys.argv[1] == "web_site_code":
            print(web_site_code())
        elif sys.argv[1] == "web_check_expire":
            print(web_check_expire())
        else:
            print("Pls sys.argv[0] web_site_discovery | web_site_code[URL] | web_check_cert | web_check_expire[IP]")
    except Exception as msg:
        print(msg)