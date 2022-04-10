#!usr/bin/env python
# -*- coding:utf-8 _*-
"""
@version:
author:xiaopengfei
@time: 2021/10/26
@file: 执行Shell两种方式.py
@function:
@modify:
"""


'''
介绍 Python 执行 Shell 的两种方式
    - os
    - subpreocess
'''

import os
import subprocess

# 使用 os 模块
def os_example():

    # 1. os.system() 返回执行后状态码
    var = os.system('ls -al')   # 执行成功返回 0
    var = os.system('ls -al xxx | 2> /dev/null')  # 失败非0，512

    if var != 0:
        print('error')


    '''
    2. os.popen 获取 Shell 返回的结果，获取内容使用:
        read()  ->  返回字符串类型的结果
        readlines()  -> 返回一个list类型的结果（可遍历）
    '''

    # read()
    var = os.popen('ls').read()
    print(var, end='')

    # readlines()
    var = os.popen('ls %s' % ('-l'))

    for line in var.readlines():
        print(line.strip().split('.'))



# 使用 subprocess 模块

'''
方法：
    call()  执行失败报错，0 成功，
    getoutput()  只能获取执行结果，返回 str 字符串（无论多少行）
    Popen()  判断是否执行成功、获取执行结果，区别是可以获取执行过程，返回 btyes 类型，需要 decode
    getstatusoutput()  判断是否执行成功、获取执行结果 ，返回 str
'''

# 若以字符串形式给出shell指令，如"ls -l "则需要使shell = Ture。否则默认以数组形式表示shell变量，如"ls","-l"
p = subprocess.Popen('netstat -tnl', stdout=subprocess.PIPE, shell=True)
out,err = p.communicate()
'''
    out -> p.read()  # bytes
    err -> p.poll    # 子进程是否执行结束
'''


# Popen
def subprocess_popen(cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    while p.poll() is None:    # Popen.poll() 检查子进程是否执行结束，没结束返回 None，结束后返回状态码
        if p.wait() is not 0:  # Popen.wait() 判断是否执行成功，命令超时后返回 TimeoutExpired 异常
            print("命令失败")
            return False
        else:
            re = p.stdout.readlines()
            for i in re:
                print(i.decode().strip())   # 原始结果进行转码，并去除\n换行

subprocess_popen("sleep 10;echo 'hello'")


'''
getstatusoutput()

    status -> 0 执行成功
    out    -> str 执行结果

'''
def subprocess_outstatus():
    status, output = subprocess.getstatusoutput('ls {0}'.format('-l'))

    for line in output.split('\n'):
        print(line)