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
        zhixinDelay_conf = parse_conf("./zhixinDelay.conf")
        self.hostname_list = []
        for item in zhixinDelay_conf:
            if(item['status'] == 1):
                self.hostname_list.append(item['hostname'])
                logging.info(self.hostname_list)
    #获取监控数据、上报告警等，此部分由具体子类改写实现。
    def monitor_alarm_proc(self):
        logging.info("task  task_id:" + str(self.last_id) + " monitor_alarm_proc start")
        #检查1小时前的
        nowtime = datetime.datetime.now() + datetime.timedelta(hours=-1)
        cutime = nowtime.strftime("%Y%m%d%H")
        logging.info(cutime)

        '''hostname = "yf-tuangou-new-web00.yf01"
        date_time = "2015020212"
        zhixinDelayThread_th = zhixinDelayThread(hostname, date_time, self.last_id)
        zhixinDelayThread_th.start()
        zhixinDelayThread_th.join()'''
        '''for hostname in self.hostname_list:
            th = aladingDelayThread(hostname, cutime, self.last_id)
            th.start()
            th.join()'''
        '''th_list = []
        for hostname in self.hostname_list:
            th = aladingDelayThread(hostname, cutime, self.last_id)
            th_list.append(th)
            th.start()
        for th in th_list:
            th.join()'''

        #最多五个机器并行计算，每个机器对应一个进程
        limit = 5
        length = len(self.hostname_list)
        cnt = None
        if(length%limit == 0):
            cnt = length/limit
        else:
            cnt = length/limit + 1
        #print cnt
        for i in xrange(cnt):
            th_list = []
            for j in xrange(limit):
                if(i*limit + j + 1 <= length):
                    #print a[i*limit + j]
                    th = aladingDelayThread(self.hostname_list[i*limit + j], cutime, self.last_id)
                    th_list.append(th)
                    th.start()
            for th in th_list:
                th.join()


        '''localFileName=self.logPre+str(cutime)
        for i in range(12):
            cmdStr = 'wget ' + self.remotePath + '/' +localFileName
            if os.system(cmdStr) == 0:
                logging.info("task  task_id:" + str(self.last_id) + " get remote log success")
                break
            logging.debug('get remote file fail at time %d', i)
            time.sleep(10)
        logging.info("task  task_id:" + str(self.last_id) + " check remote log end")
        #本地是否已有这个文件
        realFileName = os.path.realpath(localFileName)
        if not os.path.exists(realFileName):
            print 'no local file'
            exit()
        logging.info("task  task_id:" + str(self.last_id) + " check local log end")
        #分析日志文件
        totalSuccess = 0
        warn_set = set()
        log_content = dict()
        fileFp = open(realFileName, 'r')
        for line in fileFp.readlines():
            line = line.rstrip("\n")
            if 'Push Fail' in line:
                if not line in warn_set:
                    warn_set.add(line)
        logging.info("task  task_id:" + str(self.last_id) + " analyse data end")
        totalFail = len(warn_set)
        monitor_data={'log':self.remotePath + '/' +localFileName,'totalFail':str(totalFail)}
        self.add_monitor_data(self.last_id, 0, monitor_data)
        alarm_conf_id,monitorObj_id,monitorMetrics_id,name,description,status,conf = self.query_alarm_conf(self.monitorObj_id, self.monitorMetrics_id)
        for item in warn_set:
            dsc = description + 'cps push失败，请检查程序和日志，日志为：'+localFileName +"，错误提示:"+str(item)
            self.mail_send(self.subject+" "+description, dsc, self.from_mail_addr, self.to_mail_addr, self.mail_server)
            logging.info("task  task_id:" + str(self.last_id) + " mail send end")
            self.msgSend(self.phone_list, dsc , mode="qapi")
            logging.info("task  task_id:" + str(self.last_id) + " msg send end")
        logging.info("task  task_id:" + str(self.last_id) + " main func end")
        os.system("rm "+realFileName)'''
        logging.info("task  task_id:" + str(self.last_id) + " monitor_alarm_proc complete")

if __name__ == "__main__":
    log_file = "./log/" + sys.argv[0] + ".log"
    log_init(log_file)
    '''last_id = sys.argv[1]
    monitorObj_id = sys.argv[2]
    monitorMetrics_id = sys.argv[3]
    monitorMetrics_name = sys.argv[4]
    log_init(log_file)
    mymonitor = myMonitor(log_file, last_id, monitorObj_id, monitorMetrics_id, monitorMetrics_name)
    mymonitor.start()'''
    SEOMonitor_conf = parse_conf("./SEOMonitor.conf")
    monitor_result = {}
    for item in SEOMonitor_conf:
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
            data = h.request()
            '''print json.dumps(data, ensure_ascii=False)
            print data
            print expect'''
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
    print monitor_result
