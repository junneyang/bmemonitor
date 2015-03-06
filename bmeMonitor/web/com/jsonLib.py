#!/usr/bin/env python
#-*- coding: utf-8 -*-
import json

from logLib import *

def searchNode(jsonobj, id_value):
    for i,item in enumerate(jsonobj[0]['nodes']):
        if(item.has_key("nodes")):
            for j,item_item in enumerate(item['nodes']):
                if(item_item.has_key("nodes")):
                    for k,item_item_item in enumerate(item_item['nodes']):
                        if(item_item_item['id'] == id_value):
                            '''print item['text'],item_item['text'],item_item_item['text']
                            print i,j,k'''
                            return i,j,k
def queryMonitorMetrics(jsonobj):
    item_list = []
    cnt_list = []
    for item in jsonobj[0]['nodes']:
        item_tmp_cnt = 0
        if(item.has_key("nodes")):
            for item_item in item['nodes']:
                if(item_item.has_key("nodes")):
                    item_tmp_cnt += len(item_item['nodes'])
        item_list.append(item['text'])
        cnt_list.append(item_tmp_cnt)
    return [item_list, cnt_list]
if __name__ == "__main__":
    pass
