#-*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        词类 展现量 监控
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
from get_wordclass_data import *
#GetReport需要的密码
password="Nuomi20131127"
function="impression"
class myMonitor(Monitor):
    def __init__(self, log_file, last_id, monitorObj_id, monitorMetrics_id, monitorMetrics_name):
        Monitor.__init__(self, log_file, last_id, monitorObj_id, monitorMetrics_id, monitorMetrics_name)
        now_time = datetime.datetime.now()
        self.timeStamp=now_time.strftime('%Y-%m-%d-%H%M%S')
        self.dataList=list()
        self.dataDictTemp=dict()
        self.accountInfo =list()
        self.resList=list()
        self.finalresult=dict()

    #获取监控数据、上报告警等，此部分由具体子类改写实现。
    def monitor_alarm_proc(self):
        logging.info("task  task_id:" + str(self.last_id) + " monitor_alarm_proc start")
        #监控数据上报
        cutime=datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")

        #1. 查询最近四周的数据，如果没有，就调用get_wordclass脚本
        #function区分功能是  展示 impression,点击 click,消费 cost

        now_time = datetime.datetime.now()
        start_time = now_time + datetime.timedelta(days=-1)
        index=0
        while(index<=3):
            tmp = index*7
            day = start_time + datetime.timedelta(days=-tmp)#delay to index week ago
            dateStr = day.strftime('%Y-%m-%d')
            param = [dateStr]
            mysql = mysqlLib()
            ret = mysql.query_wordclass_data(param,function)
            mysql.close()
            if not ret:
                wc = WordCalss(dateStr)
                tmplist=wc.main()
                mysql = mysqlLib()
                ret = mysql.query_wordclass_data(param,function)
                mysql.close()

            #2 . 合并结果
            self.makeFinalResult(ret)
            index+=1
        logging.info("task  task_id:" + str(self.last_id) + " insert into db data_table end")

        #3. 检查报警数据并写入数据库
        #查询报警配置
        alarm_conf_id,monitorObj_id,monitorMetrics_id,name,description,status,conf = self.query_alarm_conf(self.monitorObj_id, self.monitorMetrics_id)
        #对比报警条件
        self.CreateList()
        print '2'
        self.ComputeDiff(conf['threshold'])
        print '3'
        warnList=list()
        for item in self.resList:
            cutime=datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")
            if(1 == item['flag']):
                dsc = description + " : 词类:" + str(item['wordClass']) + ", 报警:降幅超过阈值 " +str(item[function])
                print dsc
                self.add_alarm(alarm_conf_id, self.last_id, monitorObj_id,monitorMetrics_id, dsc , 0, cutime)
                warnList.append(dsc)
            '''elif(2 == item['flag']):
                dsc = description + " : 词类:" + str(item['wordClass']) + ", 报警:涨幅超过阈值 " +str(item[function])
                print dsc
                self.add_alarm(alarm_conf_id, self.last_id, monitorObj_id,monitorMetrics_id, dsc , 0, cutime)
                warnList.append(dsc)'''
        logging.info("task  task_id:" + str(self.last_id) + " monitor_alarm_proc end")

        #step 6: 发送报警邮件，短信
        for item in warnList:
            self.mail_send(self.subject+" "+description, item, self.from_mail_addr, self.to_mail_addr, self.mail_server)
        logging.info("task  task_id:" + str(self.last_id) + " mail send end")

        #报警短信
        for item in warnList:
            self.msgSend(self.phone_list, item , mode="qapi")
        logging.info("task  task_id:" + str(self.last_id) + " msg send end")

    def makeDataList(self):
        dlist=list()
        for (k,v) in self.finalresult.items():
            tmp=list()
            tmp.append(k.decode('GBK').encode('UTF-8'))
            tmp.append(v)
            dlist.append(tmp)
        return dlist

    def CreateList(self):
        try:
            count=0
            have=0
            for (k,v) in self.finalresult.items():
                tmp=k
                if(len(v)==4):
                    self.dataDictTemp[tmp]=v
                    have+=1
                else:
                    count+=1
            print '$$$$$$$$$$$$$$$$$$$$$$$$$'
            print count
            print have
        except IOError :
            print ""

    def ComputeDiff(self,threshold):
        #resList = list()#[[info, clickNum, changeNm, colorFlag],[]], colorFlag: 0:normal, 1:no normal, 2:add
        cutime=datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")
        for (k,v) in self.dataDictTemp.items():
            dataLine = v
            tempList = list()
            tempList = dataLine
            dataLine[0] =float(dataLine[0])
            dataLine[1] =float(dataLine[1])
            dataLine[2] =float(dataLine[2])
            dataLine[3] =float(dataLine[3])
            flag = 0
            if(dataLine[0] != -1 and dataLine[0] != -2  and dataLine[1] != -1 and dataLine[1] != -2):
                if(dataLine[1] == 0):
                    resChange = 1
                else:
                    resChange = float(dataLine[0] - dataLine[1])/float(dataLine[1])
                resChange = round(resChange, 2)
                if(resChange >= threshold):
                    flag = 2
                elif( resChange <= -threshold):
                    flag = 1
                tempList.append(str(resChange * 100) + '%')
            else :
                tempList.append('null')
            if(dataLine[1] != -1 and dataLine[1] != -2  and dataLine[2] != -1 and dataLine[2] != -2):
                if(dataLine[2] == 0):
                    resChange = 1
                else :
                    resChange = float(dataLine[1] - dataLine[2])/float(dataLine[2])
                resChange = round(resChange, 2)
            #   if(resChange >= 0.2 or resChange <= -0.2):
            #       flag = 1
                tempList.append(str(resChange * 100) + '%')
            else :
                tempList.append('null')
            if(dataLine[2] != -1 and dataLine[2] != -2 and dataLine[3] != -1 and dataLine[3] != -2):
                if(dataLine[3] == 0):
                    resChange = 1
                else :
                    resChange = float(dataLine[2] - dataLine[3])/float(dataLine[3])
                resChange = round(resChange, 2)
            #   if(resChange >= 0.2 or resChange <= -0.2):
            #       flag = 1
                tempList.append(str(resChange * 100) + '%')
            else :
                tempList.append('null')
            self.resList.append({function:tempList,"flag":flag,"wordClass":k})

    def makeFinalResult(self,daylist):
        for item in daylist:
            if self.finalresult.has_key(item[0]):
                self.finalresult[item[0]].append(item[1])
            else:
                self.finalresult[item[0]]=[item[1]]

    def getWordStat(self,day,function):
        wordclass=dict()
        i = 0
        while(i<len(self.accountInfo)):
                path = self.filePath + str(i)+'_'+str(day)
                print path
                if(os.path.isfile(path)):
                    inFileHandle = open(path, 'r')
                    line = inFileHandle.readline()
                    while line:
                        textLine = line.split(':')
                        line = inFileHandle.readline()
                        tmplist = str(textLine[1]).replace('[','').replace(']','').split(',')
                        impression=float(tmplist[0])
                        click=float(tmplist[1])
                        cost=float(tmplist[2])
                        tmpp = [impression,click,cost]
                        if wordclass.has_key(textLine[0]):
                            wordclass[textLine[0]] = float(wordclass[textLine[0]])+float(tmpp[function])
                            continue
                        else:
                            wordclass[textLine[0]] = float(tmpp[function])

                    inFileHandle.close();
                i+=1
        return wordclass

if __name__ == "__main__":
    log_file = "./log/" + sys.argv[0] + ".log"
    last_id = sys.argv[1]
    monitorObj_id = sys.argv[2]
    monitorMetrics_id = sys.argv[3]
    monitorMetrics_name = sys.argv[4]
    log_init(log_file)
    mymonitor = myMonitor(log_file, last_id, monitorObj_id, monitorMetrics_id, monitorMetrics_name)
    mymonitor.start()
