#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@version:
author:fly
@time: 2022/04/29
@file: test.py
@function:
@modify:
"""

import yaml
import logging.config

# 读取logger配置
with open(file='logging.yml', mode='r', encoding='utf-8') as file_logging:
    dict_conf = yaml.load(stream=file_logging, Loader=yaml.FullLoader)

# 实例化logger
logging.config.dictConfig(config=dict_conf)
logger = logging.getLogger('simpleExample')

# 打印日志
logger.debug('打印日志级别：debug')
logger.info('打印日志级别：info')
logger.warning('打印日志级别：warning')
logger.error('打印日志级别：error')
logger.critical('打印日志级别：critical')
