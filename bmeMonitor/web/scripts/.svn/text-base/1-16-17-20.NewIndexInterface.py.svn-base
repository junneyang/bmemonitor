#-*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        知心delay监控
# Purpose:
#
# Author:      caolei07
#
# Created:     21/01/2015
# Copyright:   (c) caolei07 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import sys
import time
import datetime
sys.path.append('../')
from com.logLib import *
from com.confLib import *
from com.cmdLib import *
from Monitor import Monitor
from com.mysqlLib import *
from com.httpclientLib import *
import Cookie
import httplib
import urllib
import os
import hashlib
import traceback

from aladingDelayThread import *

#json深度遍历
def find_values(id, obj):
    results = []
    def _find_values(id, obj):
        try:
            for key, value in obj.iteritems():
                if key == id:
                    results.append(value)
                elif not isinstance(value, basestring):
                    _find_values(id, value)
        except AttributeError:
            pass
        try:
            for item in obj:
                if not isinstance(item, basestring):
                    _find_values(id, item)
        except TypeError:
            pass
    if not isinstance(obj, basestring):
        _find_values(id, obj)
    return results

class myMonitor(Monitor):
    def __init__(self, log_file, last_id, monitorObj_id, monitorMetrics_id, monitorMetrics_name):
        Monitor.__init__(self, log_file, last_id, monitorObj_id, monitorMetrics_id, monitorMetrics_name)
        self.NewIndexInterface_conf = parse_conf("./NewIndexInterface.conf")
    #获取监控数据、上报告警等，此部分由具体子类改写实现。
    def monitor_alarm_proc(self):
        logging.info("task  task_id:" + str(self.last_id) + " monitor_alarm_proc start")
        monitor_result = {}
        for item in self.NewIndexInterface_conf:
            desc = item['desc']
            interface = item['interface']
            ip_port = item['ip_port']
            url = item['url']
            method = item['method']
            params = item['params']
            expect = item['expect']
            compare = item['compare']
            flag = item['flag']
            data = None
            monitor_result[interface] = {"status":0,"msg":"ok"}
            if(flag == 1):
                #print params
                h = httpclientLib(ip_port, url, method=method, params=params)
                status,data = h.request()
                if(status != 200):
                    monitor_result[interface] = {"status":-1,"msg":url + " access exception"}
                    continue
                try:
                    print json.dumps(data, ensure_ascii=False)
                    print data
                    print expect
                    logging.info("****************" + desc + "****************")
                    logging.info(json.dumps(data, ensure_ascii=False))
                    logging.info(json.dumps(expect, ensure_ascii=False))
                    tmp = json.dumps(data, ensure_ascii=False)
                    #print tmp
                    values =  find_values('url', json.loads(tmp))
                    error_item_list = []
                    for item in values:
                        #print item
                        h = httpclientLib(ip_port, url, method=method, params=params)
                        status,data = h.request()
                        if(status != 200):
                            error_item_list.append(item)
                    if(len(error_item_list) != 0):
                        monitor_result[interface] = {"status":-1,"msg":error_item_list}
                except Exception as e:
                    monitor_result[interface] = {"status":-1,"msg":"response exception"}
        #print monitor_result
        logging.info(json.dumps(monitor_result))
        total = 0
        normal = 0
        exception = 0
        for item in monitor_result:
            total += 1
            if(monitor_result[item]['status'] == 0):
                normal += 1
            else:
                exception += 1
        mysql = mysqlLib()
        uptime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        param = (total, normal, exception, json.dumps(monitor_result), uptime, "NewIndex")
        mysql.update_tbl_seo(param)
        mysql.close()
        logging.info("task  task_id:" + str(self.last_id) + " monitor_alarm_proc complete")


if __name__ == "__main__":
    log_file = "./log/" + sys.argv[0] + ".log"
    last_id = sys.argv[1]
    monitorObj_id = sys.argv[2]
    monitorMetrics_id = sys.argv[3]
    monitorMetrics_name = sys.argv[4]
    log_init(log_file)
    mymonitor = myMonitor(log_file, last_id, monitorObj_id, monitorMetrics_id, monitorMetrics_name)
    mymonitor.start()
    '''log_file = "./log/" + sys.argv[0] + ".log"
    log_init(log_file)
    NewIndexInterface_conf = parse_conf("./NewIndexInterface.conf")
    monitor_result = {}
    for item in NewIndexInterface_conf:
        desc = item['desc']
        interface = item['interface']
        ip_port = item['ip_port']
        url = item['url']
        method = item['method']
        params = item['params']
        expect = item['expect']
        compare = item['compare']
        flag = item['flag']
        data = None
        monitor_result[interface] = {"status":0,"msg":"ok"}
        if(flag == 1):
            #print params
            h = httpclientLib(ip_port, url, method=method, params=params)
            status,data = h.request()
            if(status != 200):
                monitor_result[interface] = {"status":-1,"msg":url + " access exception"}
                continue
            try:
                print json.dumps(data, ensure_ascii=False)
                print data
                print expect
                logging.info("****************" + desc + "****************")
                logging.info(json.dumps(data, ensure_ascii=False))
                logging.info(json.dumps(expect, ensure_ascii=False))
                tmp = json.dumps(data, ensure_ascii=False)
                #print tmp
                values =  find_values('url', json.loads(tmp))
                error_item_list = []
                for item in values:
                    #print item
                    h = httpclientLib(ip_port, url, method=method, params=params)
                    status,data = h.request()
                    if(status != 200):
                        error_item_list.append(item)
                if(len(error_item_list) != 0):
                    monitor_result[interface] = {"status":-1,"msg":error_item_list}
            except Exception as e:
                monitor_result[interface] = {"status":-1,"msg":"response exception"}
    print monitor_result'''
