#-*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        cps server 验券 监控
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
    remotePath = 'ftp://hz01-nuomi-union.hz01/home/nuomi/bmescript/cps/log'
    logPre = 'loadVerifyData.log.'
    def __init__(self, log_file, last_id, monitorObj_id, monitorMetrics_id, monitorMetrics_name):
        Monitor.__init__(self, log_file, last_id, monitorObj_id, monitorMetrics_id, monitorMetrics_name)
        self.dataList = list()
    #获取监控数据、上报告警等，此部分由具体子类改写实现。
    def monitor_alarm_proc(self):
        logging.info("task  task_id:" + str(self.last_id) + " monitor_alarm_proc start")
        #检查五分钟前的
        nowtime = datetime.datetime.now()+datetime.timedelta(minutes=-5)
        cutime_0 = nowtime.strftime("%Y-%m-%d_%H-%M")
        cutime_1 = (nowtime + datetime.timedelta(minutes=-1)).strftime("%Y-%m-%d_%H-%M")
        #该脚本每两分钟跑一次，每隔十秒检查一次，直到发现日志文件，若运行超过两分钟报警
        localFileName0=self.logPre+str(cutime_0)
        localFileName1=self.logPre+str(cutime_1)
        #localFileName0='loadVerifyData.log.2014-12-30_01-59'
        for i in range(12):
            cmdStr = 'wget ' + self.remotePath + '/' +localFileName0
            if os.system(cmdStr) == 0:
                logging.info("task  task_id:" + str(self.last_id) + " get remote log success")
                break
            cmdStr = 'wget ' + self.remotePath + '/' +localFileName1
            if os.system(cmdStr) == 0:
                logging.info("task  task_id:" + str(self.last_id) + " get remote log success")
                break
            logging.debug('get remote file fail at time %d', i)
            time.sleep(10)
        logging.info("task  task_id:" + str(self.last_id) + " check remote log end")
        #本地是否已有这个文件
        realFileName0 = os.path.realpath(localFileName0)
        realFileName1 = os.path.realpath(localFileName1)
        if os.path.exists(realFileName0):
            localRealFile = realFileName0
            LocalRelaFile = localFileName0
        elif os.path.exists(realFileName1):
            localRealFile = realFileName1
            LocalRelaFile = localFileName1
        else:
            exit()
            logging.debug("task  task_id:" + str(self.last_id) + " check remote log end")
        logging.info("task  task_id:" + str(self.last_id) + " check local log end")
        #分析日志文件
        #准备数据，存入字典
        log_content = dict()
        fileFp = open(localRealFile, 'r')
        for line in fileFp.readlines():
            line = line.rstrip("\n")
            couponInfo = line.split(']')
            if len(couponInfo)!=2:
            #格式不正确
                continue
            title = str(couponInfo[0])[1:]
            info = str(couponInfo[1])[1:]
            log_content[info]=title
        logging.info("task  task_id:" + str(self.last_id) + " prepare data end")
        #把日志名存入data表
        self.add_monitor_data(self.last_id, 0, self.remotePath+"/"+LocalRelaFile)
        for (k,v) in log_content.items():
            a=v.split(' ')
            hint = a[5]
            if(str(hint)=='WARNING'):
                alarm_conf_id,monitorObj_id,monitorMetrics_id,name,description,status,conf = self.query_alarm_conf(self.monitorObj_id, self.monitorMetrics_id)
                dsc = description + 'cps 验券检查出错，请检查程序和日志，日志为：'+LocalRelaFile +"，错误提示:【"+str(v)+"】"+str(k)
                cutime=datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")
                #####################################添加告警，暂时屏蔽-by yangjun03############################################################
                #self.add_alarm(alarm_conf_id, self.last_id, monitorObj_id,monitorMetrics_id, dsc , 0, cutime)
                #####################################添加告警，暂时屏蔽-by yangjun03############################################################
                self.mail_send(self.subject+" "+description, dsc, self.from_mail_addr, self.to_mail_addr, self.mail_server)
                logging.info("task  task_id:" + str(self.last_id) + " mail send end")
                self.msgSend(self.phone_list, dsc , mode="qapi")
                logging.info("task  task_id:" + str(self.last_id) + " msg send end")
        logging.info("task  task_id:" + str(self.last_id) + " main func end")
        os.system("rm "+localRealFile)

if __name__ == "__main__":
    log_file = "./log/" + sys.argv[0] + ".log"
    last_id = sys.argv[1]
    monitorObj_id = sys.argv[2]
    monitorMetrics_id = sys.argv[3]
    monitorMetrics_name = sys.argv[4]
    log_init(log_file)
    mymonitor = myMonitor(log_file, last_id, monitorObj_id, monitorMetrics_id, monitorMetrics_name)
    mymonitor.start()
