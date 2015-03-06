#-*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        url监控
# Purpose:
#
# Author:      caolei07
#
# Created:     23/01/2015
# Copyright:   (c) caolei07 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

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
#from monitorurl import *
from check_url import *

#GetReport需要的密码
password="Nuomi20131127"

class myMonitor(Monitor):
    def __init__(self, log_file, last_id, monitorObj_id, monitorMetrics_id, monitorMetrics_name):
        Monitor.__init__(self, log_file, last_id, monitorObj_id, monitorMetrics_id, monitorMetrics_name)
        now_time = datetime.datetime.now()
        self.dataList=list()
        self.accountInfo =list()

    #获取监控数据、上报告警等，此部分由具体子类改写实现。
    def monitor_alarm_proc(self):
        mysql = AccountInfo()
        self.accountInfo =mysql.get_tbl_accountinfo()
        mysql.save_tbl_accountinfo()
        mysql.save_tbl_cid()
        mysql.close()
        logging.info("task  task_id:" + str(self.last_id) + " monitor_alarm_proc start")
        #监控数据上报
        now_time = datetime.datetime.now()
        day = now_time + datetime.timedelta(days=-1)
        dateStr = day.strftime('%Y-%m-%d')

        index=0
        th_list = []
        while(index<len(self.accountInfo)):
            myMonitor = MyUrlMonitor(dateStr,self.accountInfo[index],self.last_id)
            th_list.append(myMonitor)
            myMonitor.start()
            index+=1

        for item in th_list:
            item.join()
        logging.info("task  task_id:" + str(self.last_id) + " all thread run end")

        #检查报警
        mysql = mysqlLib()
        alarm_conf_id,monitorObj_id,monitorMetrics_id,name,description,status,conf = self.query_alarm_conf(self.monitorObj_id, self.monitorMetrics_id)
        #对比报警条件
        print conf['threshold']
        param=[dateStr,conf['threshold']]
        warnList = mysql.query_urlalarm_data(param)
        alarmList = list()
        if(len(warnList)==0):
            mysql.close()
            return 'close'
        for item in warnList:
            accountName=item[2]
            totalurlNum=item[3]
            errorurlNum=item[4]
            deadDealNum=item[5]
            badDeadDealNum=item[6]
            openurlErrorNum=item[7]
            noListResultNum=item[8]
            errorCidNum=item[9]
            formatErrorNum=item[10]
            nullUrlNum=item[11]

            dsc = description + " 帐户名：" + str(accountName) + ",Url总数:"+str(totalurlNum)+",Error总数:"+str(errorurlNum)+",过期团单:"+str(deadDealNum)+",非合理过期团单:"+str(badDeadDealNum)+",访问错误:"+str(openurlErrorNum)+",无搜索结果:"+str(noListResultNum)+",非天兔Cid:"+str(errorCidNum)+",URL格式错误:"+str(formatErrorNum)+",空URL:"+str(nullUrlNum)
            alarmList.append(dsc)
            cutime=datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")
            self.add_alarm(alarm_conf_id, self.last_id, monitorObj_id,monitorMetrics_id, dsc , 0, cutime)
        logging.info("task  task_id:" + str(self.last_id) + " insert into db alarm_table end")

        mysql.close()

        #step 6: 发送报警邮件，短信
        for item in alarmList:
            self.mail_send(self.subject+" "+description, str(item), self.from_mail_addr, self.to_mail_addr, self.mail_server)
        logging.info("task  task_id:" + str(self.last_id) + " mail send end")
        #报警短信
        for item in warnList:
            self.msgSend(self.phone_list, str(item) , mode="qapi")
        logging.info("task  task_id:" + str(self.last_id) + " msg send end")

if __name__ == "__main__":
    log_file = "./log/" + sys.argv[0] + ".log"
    last_id = sys.argv[1]
    monitorObj_id = sys.argv[2]
    monitorMetrics_id = sys.argv[3]
    monitorMetrics_name = sys.argv[4]
    log_init(log_file)
    mymonitor = myMonitor(log_file, last_id, monitorObj_id, monitorMetrics_id, monitorMetrics_name)
    mymonitor.start()
