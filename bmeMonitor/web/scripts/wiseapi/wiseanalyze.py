#! /usr/bin/env python
# -*- coding:UTF-8 -*-
# Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved
# 2014-10-17 21:11:06 chengyunlai
'''
@file wise.wiseanalyze.py
@author chengyunlai (chengyunlai@baidu.com)
@date 2014-10-17 21:11:06
@brief 
'''

import sys

def calc_relate(text, sample):
    text = text.replace('团购', '').decode('utf8')
    # 如果超过7个字符，截断保留7个字符
    if len(text) > 7:
        text = text[0:7]
    c = len(sample)
    resStr = ''
    for s in sample:
        s = s.decode('utf8')
        if s.find(text) >= 0: 
            c -= 1
            resStr += s + ";"
            
    if c == 0: return (1, resStr)        
    else: return (0, '')

def execute(ralFile):
    with open(ralFile, 'r') as fin:
        cards = fin.readlines()
    # 统计参数
    allCount, noretCount, topCount, matchCount = 0, 0, 0, 0  # 总数，无召回，置顶数，相关数
    for card in cards:
        card = eval(card.strip())
        if card['tpos'] <= 0: 
            card['relate'] = 0
            card['rpos'] = -1
            card['deals'] = ''
        else: 
            rel, mat = calc_relate(card['query'], card['deals'])
            card['relate'] = rel
            card['deals'] = mat.encode('utf-8')
        print "%d\t%d\t%s\t%s\t%s" % (card['rpos'], \
             card['relate'], card['city'], card['query'], card['deals'])
        allCount += 1
        if card['rpos'] < 0: noretCount = noretCount + 1
        if card['rpos'] == 1: topCount += 1
        if card['relate'] == 1:matchCount += 1
    
    print ''
    print 'All Count = ' , allCount
    print 'No result Count = ', noretCount
    print 'Near Top Count = ', topCount
    print 'Match Count = ', matchCount
    
    # for card in cards:
    pass

if __name__ == '__main__':
    if len(sys.argv) < 2: 
        # print  "Please 给出输入文件"
        # exit(-1)
        execute('data/res.out')
    else:
        execute(sys.argv[1])
   
    # a="琪丽美甲团购 "
    # b=["琪丽美甲美甲基础护理1次！精心呵护，完美演绎￥9.9￥20已售0", "琪丽美甲美甲套餐！专业的美甲技师，经验丰富！￥38￥170已售19", "琪丽美甲美甲2次套餐！细心的打理！￥69￥120已售1"]
    # print calc_relate(a,b)
