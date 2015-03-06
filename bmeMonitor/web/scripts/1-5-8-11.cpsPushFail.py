#-*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        cps push push失败 监控
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
import Cookie
import httplib
import urllib
import os
import hashlib
import traceback

class myMonitor(Monitor):
    remotePath = 'ftp://nj02-nuomi-cps02.nj02/home/nuomi/cps-push/log'
    logPre = 'cpsPush.log.'
    def __init__(self, log_file, last_id, monitorObj_id, monitorMetrics_id, monitorMetrics_name):
        Monitor.__init__(self, log_file, last_id, monitorObj_id, monitorMetrics_id, monitorMetrics_name)
        self.dataList = list()
    #获取监控数据、上报告警等，此部分由具体子类改写实现。
    def monitor_alarm_proc(self):
        logging.info("task  task_id:" + str(self.last_id) + " monitor_alarm_proc start")
        #检查1小时前的
        nowtime = datetime.datetime.now()+datetime.timedelta(hours=-12)
        cutime = nowtime.strftime("%Y-%m-%d_%H")

        localFileName=self.logPre+str(cutime)
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
        os.system("rm "+realFileName)

if __name__ == "__main__":
    log_file = "./log/" + sys.argv[0] + ".log"
    last_id = sys.argv[1]
    monitorObj_id = sys.argv[2]
    monitorMetrics_id = sys.argv[3]
    monitorMetrics_name = sys.argv[4]
    log_init(log_file)
    mymonitor = myMonitor(log_file, last_id, monitorObj_id, monitorMetrics_id, monitorMetrics_name)
    mymonitor.start()
