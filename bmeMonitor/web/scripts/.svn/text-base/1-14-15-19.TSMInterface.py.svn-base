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

class myMonitor(Monitor):
    def __init__(self, log_file, last_id, monitorObj_id, monitorMetrics_id, monitorMetrics_name):
        Monitor.__init__(self, log_file, last_id, monitorObj_id, monitorMetrics_id, monitorMetrics_name)
        self.TSMInterface_conf = parse_conf("./TSMInterface.conf")
    #获取监控数据、上报告警等，此部分由具体子类改写实现。
    def monitor_alarm_proc(self):
        logging.info("task  task_id:" + str(self.last_id) + " monitor_alarm_proc start")
        monitor_result = {}
        for item in self.TSMInterface_conf:
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
            if(flag == 1):
                #print params
                h = httpclientLib(ip_port, url, method=method, params=params)
                status,data = h.request()
                '''print json.dumps(data, ensure_ascii=False)
                print data
                print expect'''
                try:
                    logging.info("****************" + desc + "****************")
                    logging.info(json.dumps(data, ensure_ascii=False))
                    logging.info(json.dumps(expect, ensure_ascii=False))
                    if(compare == 1):
                        if(data['data'] == expect['data']):
                            monitor_result[interface] = {"status":0,"msg":"ok"}
                        else:
                            monitor_result[interface] = {"status":-1,"msg":"expect:\n"+json.dumps(expect, ensure_ascii=False)+"\ndata:\n"+json.dumps(data, ensure_ascii=False)}
                    else:
                        if(data['errno'] == 0):
                            monitor_result[interface] = {"status":0,"msg":"ok"}
                        else:
                            monitor_result[interface] = {"status":-1,"msg":"errno not 0:\n"+json.dumps(data, ensure_ascii=False)}
                except Exception as e:
                    monitor_result[interface] = {"status":-1,"msg":"response data error"}
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
        param = (total, normal, exception, json.dumps(monitor_result), uptime, "TSM")
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
