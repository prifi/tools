#!/usr/bin/env python
#coding=utf-8
'''
    Suprevisord Listener example.
'''
import requests
import sys
import os
import socket

# baojing
hostname = socket.gethostname()
## SupplyChainRebot
#robotUrl = ""
## DressRebot
robotUrl = ""


def write_stdout(s):
    sys.stdout.write(s)
    sys.stdout.flush()

def write_stderr(s):
    sys.stderr.write(s)
    sys.stderr.flush()

def baojing(msg=None, data=None):
    if msg == None and data == None:
        return
    # alert
    formatStr = '''【告警】<font color=\"warning\">`{0}`</font> \n
        ><font color=\"comment\">当前主机: {1}</font>'''.format(msg, hostname)

    data = {
        "msgtype": "markdown",
        "markdown": {
            "content": formatStr
        }
    }
    requests.post(robotUrl, json=data)

def parseData(data):
    tmp = data.split('\n')
    pheaders = dict([ x.split(':') for x in tmp[0].split() ])
    pdata = None
    if len(tmp) > 1:
        pdata = tmp[1]
    return pheaders, pdata

def main():
    #Only supervisord can run this listener, otherwise exit.
    if not 'SUPERVISOR_SERVER_URL' in os.environ:
        print "%s must be run as a supervisor listener." % sys.argv[0]
        return

    while True:
        #echo 'READY' and wait for event for stdin.
        write_stdout('READY\n')
        line = sys.stdin.readline()  # read header line from stdin
        headers = dict([ x.split(':') for x in line.split() ])
        data = sys.stdin.read(int(headers['len'])) # read the event payload

        if headers['eventname'] == 'PROCESS_STATE_EXITED' or\
           headers['eventname'] == 'PROCESS_STATE_FATAL' or\
           headers['eventname'] == 'PROCESS_STATE_STOPPED':
            pheaders, pdata = parseData(data)
            from_state = pheaders['from_state']
            process_name = pheaders['processname']
            if headers['eventname'] == 'PROCESS_STATE_EXITED' and\
                not int(pheaders['expected']):
                msg = '进程 %s(PID: %s) 异常退出，请检查进程状态.'\
                    % (process_name, pheaders['pid'])
                baojing(msg=msg)
            if headers['eventname'] == 'PROCESS_STATE_FATAL':
                msg = '进程 %s 启动失败，请检查进程状态.'\
                    % (process_name)
                baojing(msg=msg)
        elif headers['eventname'] == 'PROCESS_LOG_STDERR':
            pheaders, pdata = parseData(data)
            process_name = pheaders['processname']
            pid = pheaders['pid']
            msg = '进程 %s(PID: %s) 错误输出，请检查进程状态，错误输出信息: %s.' \
                % (process_name, pid, pdata)
            baojing(msg=msg)
        #echo RESULT
        write_stdout('RESULT 2\nOK') # transition from READY to ACKNOWLEDGED

if __name__ == '__main__':
    main()
