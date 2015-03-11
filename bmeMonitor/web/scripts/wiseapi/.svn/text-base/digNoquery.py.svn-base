#! /usr/bin/env python
# -*- coding:UTF-8 -*-
# Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved
# 2014-10-16 20:01:58 chengyunlai
'''
@file wise.digNoquery.py
@author chengyunlai (chengyunlai@baidu.com)
@date 2014-10-16 20:01:58
@brief 
'''

from wise.const_cookie import provice_loc_map
from wisetuan import WiseRunner
import ConfigParser

# 加载系统配置
SYS_CONF = 'wise.conf'
syscfg = ConfigParser.ConfigParser()
syscfg.read(SYS_CONF)

def main():
    # 读取queries
    with open(syscfg.get('request', 'queries'), 'r') as fin:
        qlines = fin.readlines()
    queries = []
    for ql in qlines:
        ql = ql.strip()
        if not ql:continue
        ql = ql.split('##')
        if len(ql) < 2:continue
        queries.append(ql)
    #    
    print 'Length of query = %d' % len(queries)
    print 'Start running ...... '
    #
    runner = WiseRunner(queries, provice_loc_map, syscfg)
    runner.start()

if __name__ == '__main__':
    main()
