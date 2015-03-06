#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import time
import datetime
from accountinfo import *
sys.path.append('../')
sys.path.append('/statpy/')
from com.logLib import *
from com.confLib import *
from com.cmdLib import *
from Monitor import Monitor
from com.mysqlLib import *
from statpy.ApiSDKSoapClient import ApiSDKSoapClient
from statpy.ApiSDKSoapClient import printSoapResponse
from statpy.sms_v3_ReportService import *
from statpy.sms_v3_AccountService import *

#GetReport需要的密码
password="Nuomi20131127"

class myMonitor(Monitor):
    def __init__(self, log_file, last_id, monitorObj_id, monitorMetrics_id, monitorMetrics_name):
        Monitor.__init__(self, log_file, last_id, monitorObj_id, monitorMetrics_id, monitorMetrics_name)
        self.account = list()

    #获取监控数据、上报告警等，此部分由具体子类改写实现。
    def monitor_alarm_proc(self):
        logging.info("task  task_id:" + str(self.last_id) + " monitor_alarm_proc start")

        #step 1: 得到数据库的账户信息
        mysql = AccountInfo()
        self.account =mysql.get_tbl_accountinfo()
        logging.info("task  task_id:" + str(self.last_id) + " get local accountinfo end")

        #step 2: 调用凤巢api返回余额数据
        balanceList = []  # 记录结果
        #调用凤巢api返回余额数据
        for accountItem in self.account :
            strtemp = self.GetReport(accountItem, password)
            cutime=datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")
            dictMerged={"balance":strtemp,"datetime":cutime,"accountName":accountItem[0]}
            balanceList.append(dictMerged)
            time.sleep(1)
            if(strtemp != None and strtemp!=''):
                break
        logging.info("task  task_id:" + str(self.last_id) + " get balance data end")

        #step 3: 存入本地数据库
        self.add_monitor_data(self.last_id, 0, balanceList)
        logging.info("task  task_id:" + str(self.last_id) + " insert into tbl_monitordata end")

        #step 4: 报警
        alarm_conf_id,monitorObj_id,monitorMetrics_id,name,description,status,conf = self.query_alarm_conf(self.monitorObj_id, self.monitorMetrics_id)
        #对比报警条件
        warnList = []  # 记录结果
        for item in balanceList:
            if(conf['threshold'] > item['balance']):
                cutime=datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")
                dsc = description + " : " + " 截止"+str(cutime)+"，账户余额为"+str(item['balance'])+"元，小于报警阈值" + str(conf['threshold']) + "元，请尽快充值！"
                self.add_alarm(alarm_conf_id, self.last_id, monitorObj_id,monitorMetrics_id, dsc , 0, cutime)
                warnList.append(dsc)
        logging.info("task  task_id:" + str(self.last_id) + " monitor_alarm_proc end")

        #报警邮件
        for item in warnList:
            self.mail_send(self.subject+" "+description, item, self.from_mail_addr, self.to_mail_addr, self.mail_server)
        logging.info("task  task_id:" + str(self.last_id) + " mail send end")
        #报警短信
        for item in warnList:
            self.msgSend(self.phone_list, item , mode="qapi")
        logging.info("task  task_id:" + str(self.last_id) + " msg send end")

    def GetReport(self, accountInfo, passwdStr=None):
        try:
            accountService = sms_v3_AccountService()
            accountService.setUsername(accountInfo[0])
            accountService.setPassword(accountInfo[4])
            accountService.setToken(accountInfo[1])

            accountInfo = accountService.getAccountInfo()
            getNum = 0
            while (accountInfo is None or accountInfo['body'] is None or accountInfo['body']['accountInfoType'] is None):
                time.sleep(5)
                if(getNum > 12):
                    break
                getNum += 1
                accountInfo = accountService.getAccountInfo()
            if (getNum > 12):
                print "Get Professional Report Id fail!\n"
                return '*'
            #print accountInfo['body']['accountInfoType']
            balanceValue = accountInfo['body']['accountInfoType']['balance']
            return balanceValue
        except Exception, e:
            print e
            tb.print_exc()
            return -1

if __name__ == "__main__":
    log_file = "./log/" + sys.argv[0] + ".log"
    last_id = sys.argv[1]
    monitorObj_id = sys.argv[2]
    monitorMetrics_id = sys.argv[3]
    monitorMetrics_name = sys.argv[4]
    log_init(log_file)
    mymonitor = myMonitor(log_file, last_id, monitorObj_id, monitorMetrics_id, monitorMetrics_name)
    mymonitor.start()
