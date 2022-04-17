# -*- coding: utf-8 -*-
# @Author: fly
# @Date:   2022-04-11 16:26:15
# @Last Modified by:   fly
# @Last Modified time: 2022-04-11 16:27:14

# https://www.osgeo.cn/cpython/library/optparse.html

import optparse

parser = optparse.OptionParser()

# dest 存储字段，type 指定参数类型, metavar 提醒参数大写
parser.add_option("-n", "--number", dest="number", help='test args', default='12', type=int, metavar="NUM")

parser.add_option("-f", "--file", dest="filename", help="write report to FILE", metavar="FILE")

(options, args) = parser.parse_args()
print(options.number)   # 12

# store_false 解析到 -q，会被赋予 False 值。 对应 store_true
parser.add_option("-q", "--quiet",
                  action="store_false", dest="verbose", default=True,
                  help="don't print status messages to stdout")

(options, args) = parser.parse_args()

# python test.py
print(options.verbose)  # True