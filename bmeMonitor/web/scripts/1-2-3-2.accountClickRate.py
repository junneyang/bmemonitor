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

def IsValidRealTimeUserClickRet( clickRet ) :
    """ 检查API查询账户点击结果 是否合法
    Args:
        clickRet:  API请求账户点击返回的数据

    Returns:
        如果检测通过，返回True; 否则返回False.
    """
    if clickRet is None : return False
    if type(clickRet)!=dict : return False
    if not clickRet.has_key('body') : return False

    bd = clickRet['body']
    if bd is None : return False
    if type(bd)!=dict : return False
    if not bd.has_key('realTimeResultTypes') : return False

    rli = bd['realTimeResultTypes']
    if len(rli)==0: return False
    return True
def GetReport(startTime, endTime, startHour, endHour, accountInfo, passwdStr):
    """ 请求账户点击数据

    Args:
        startTime   : 开始时间
        endTime     : 结束时间
        startHour   :
        endHour     :
        accountInfo : 账户信息
        passwdStr   : 账户密码

    Returns:

    """
    try:
        if accountInfo[0] == "baidu-短语商家2140114":
            passwdStr = "Ab1234567890"
        else:
            passwdStr = "Nuomi20131127"

        service = sms_v3_ReportService()
        service.setUsername(accountInfo[0])
        service.setPassword(passwdStr)
        service.setToken(accountInfo[1])
        #service.setTarget(accountInfo[0])

        strStartDate = startTime + 'T' + '00:00:00.000'
        strEndDate = endTime + 'T' + '23:59:59.000'

        print '~~~~~~~~~~~  华丽的分割 ~~~~~~~~~~~~~~~~~~~'
        print accountInfo[0]            # 打印 帐户名
        print strStartDate, strEndDate  # 查询监控时间范围

        # 准备请求参数
        request = {
                "realTimeRequestTypes":{
                        "performanceData":["click", "impression"],
                        "startDate" : strStartDate,
                        "endDate" : strEndDate,
                        "levelOfDetails" : 2,
                        "reportType" : 2,
                        "statRange":2,
                        "statIds":None,
                        "unitOfTime":7,
                        "device":0
                }
        }
        getRealTimeReportResList = None     # API调用结果保存
        getNum = 0                          # API 重试调用次数
        MAX_RETRY = 2                       # 允许重试阈值，超过则报警
        SLEEP_TIME = 3                      # API调用重试时间间隔/秒

        while not IsValidRealTimeUserClickRet(getRealTimeReportResList):
            getNum += 1
            if(getNum > MAX_RETRY):
                break
            if getNum > 1 : time.sleep(SLEEP_TIME)
            # 调用API
            getRealTimeReportResList = service.getRealTimeData(request)

        print ''
        #print getRealTimeReportResList['header']
        print getRealTimeReportResList
        print ''

        if ( getNum > MAX_RETRY):
            print "Get Professional Report Id fail!\n"
            return '*'

        clickSum = 0
        time1 = startTime + " " + startHour
        time2 = endTime + " " + endHour
        flag = 0
        listInfo = getRealTimeReportResList['body']['realTimeResultTypes']
        for itemInfo in listInfo:
            if(cmp(itemInfo['date'], time1) == 0 or cmp(itemInfo['date'], time2) == 0):
                flag = 1
                clickSum += int(itemInfo['kpis'][0])

        if(flag == 1):
            return str(clickSum)
        else:
            return ''
    except Exception, e:
        print e
        tb.print_exc()


class myMonitor(Monitor):
    def __init__(self, log_file, last_id, monitorObj_id, monitorMetrics_id, monitorMetrics_name):
        Monitor.__init__(self, log_file, last_id, monitorObj_id, monitorMetrics_id, monitorMetrics_name)
        self.account = list()
        self.dataList = list()
        self.dataListTemp = list()
        self.resList = list()
    #获取监控数据、上报告警等，此部分由具体子类改写实现。
    def monitor_alarm_proc(self):
        logging.info("task  task_id:" + str(self.last_id) + " monitor_alarm_proc start")
        cutime=datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")

        #step 1: 得到数据库的账户信息
        mysql = AccountInfo()
        self.account =mysql.get_tbl_accountinfo()
        logging.info("task  task_id:" + str(self.last_id) + " get local accountinfo end")

        #step 2: 调用凤巢api返回余额数据
        #1. 准备时间数据
        now_time = datetime.datetime.now()
        now_time = now_time + datetime.timedelta(hours=-4)#delay to 4hours ago
        startHourStr = now_time.strftime('%H')
        dateStr = now_time.strftime('%Y-%m-%d')
        yes_time_first_start = now_time.strftime('%Y-%m-%d')    # 本周
        yes_time = now_time + datetime.timedelta(days=-7)       # 前一周同时段
        yes_time_second_start = yes_time.strftime('%Y-%m-%d')
        yes_time = now_time + datetime.timedelta(days=-14)      # 前两周同时段
        yes_time_third_start = yes_time.strftime('%Y-%m-%d')
        yes_time = now_time + datetime.timedelta(days=-21)      # 前三周同时段
        yes_time_fourth_start = yes_time.strftime('%Y-%m-%d')
        yes_hour_end_temp = now_time + datetime.timedelta(hours=1)  # 结束时间
        endHourStr = yes_hour_end_temp.strftime('%H')
        yes_time_first_end = yes_hour_end_temp.strftime('%Y-%m-%d')
        yes_time = yes_hour_end_temp + datetime.timedelta(days=-7)
        yes_time_second_end = yes_time.strftime('%Y-%m-%d')
        yes_time = yes_hour_end_temp + datetime.timedelta(days=-14)
        yes_time_third_end = yes_time.strftime('%Y-%m-%d')
        yes_time = yes_hour_end_temp + datetime.timedelta(days=-21)
        yes_time_fourth_end = yes_time.strftime('%Y-%m-%d')
        #2. 查询点击率
        clickList = list()
        for accountItem in self.account :
            tempList = list()
            strtemp =GetReport(yes_time_first_start, yes_time_first_end,
            startHourStr, endHourStr, accountItem, password)
            tempList.append(strtemp)
            time.sleep(1)

            strtemp = GetReport(yes_time_second_start, yes_time_second_end,
            startHourStr, endHourStr, accountItem, password)
            tempList.append(strtemp)
            time.sleep(1)

            strtemp = GetReport(yes_time_third_start, yes_time_third_end,
            startHourStr, endHourStr, accountItem, password)
            tempList.append(strtemp)
            time.sleep(1)

            strtemp = GetReport(yes_time_fourth_start, yes_time_fourth_end,
            startHourStr, endHourStr, accountItem, password)
            tempList.append(strtemp)
            #tempList格式 [本周,前一周同时段,前两周同时段,前三周同时段]
            cutime=datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")
            dictMerged={"clickrate":tempList,"datetime":cutime,"accountName":accountItem[0]}
            self.dataList.append(dictMerged)
        logging.info("task  task_id:" + str(self.last_id) + " get click data end")

        #step 3: 存入本地数据库
        self.add_monitor_data(self.last_id, 0, self.dataList)
        logging.info("task  task_id:" + str(self.last_id) + " insert into tbl_monitordata end")

        #step 4: 报警
        #查询报警配置
        alarm_conf_id,monitorObj_id,monitorMetrics_id,name,description,status,conf = self.query_alarm_conf(self.monitorObj_id, self.monitorMetrics_id)
        warnList = []  # 记录结果
        #预处理，防止有无数据的情况
        self.CreateList()
        self.ComputeDiff(conf['threshold'], conf['base'])
        for item in self.resList:
            cutime=datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")
            tmp = float(conf['threshold'])
            value = str(tmp*100)+'%'
            #暂时屏蔽涨幅超过阈值告警
            '''if(1 == item['flag']):
                dsc = description + "：涨幅超过阈值" +value +"，账户名:" + str(item['accountName']).decode('utf-8') + "，检查时段："+startHourStr+":00-"+endHourStr+":00，数据如下："+str(item['clickrate'])
                self.add_alarm(alarm_conf_id, self.last_id, monitorObj_id,monitorMetrics_id, dsc , 0, cutime)
                warnList.append(dsc)'''
            if(2 == item['flag']):
                dsc = description + "：降幅超过阈值" +value +"，账户名:" + str(item['accountName']).decode('utf-8') + "，检查时段："+startHourStr+":00-"+endHourStr+":00，数据如下："+str(item['clickrate'])
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

    def CreateList(self):
        try:
            for item in self.dataList:
                linelist = item['clickrate']
                tempData = list()
                for line in linelist:
                    if(line is None or cmp(line, '') == 0):
                        tempData.append(-1)
                    elif(cmp(line, '*') == 0):
                        tempData.append(-2)
                    else :
                        tempData.append(int(line))
                self.dataListTemp.append({"click":tempData,"datetime":item['datetime'],"accountName":item['accountName']})
        except IOError :
            print "have no click this time!"

    def ComputeDiff(self,threshold,base):
        #resList = list()#[[info, clickNum, changeNm, colorFlag],[]], colorFlag: 0:normal, 1:no normal, 2:add
        i = 0
        for line in self.dataListTemp:
            dataLine = line['click']
            tempList = list()
            tempList = dataLine
            flag = 0
            if(dataLine[0] >= base and dataLine[1] >= base and dataLine[2] >= base and dataLine[3] >= base):
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
            self.resList.append({"clickrate":tempList,"flag":flag,"accountName":line['accountName'],"datetime":line['datetime']})

if __name__ == "__main__":
    log_file = "./log/" + sys.argv[0] + ".log"
    last_id = sys.argv[1]
    monitorObj_id = sys.argv[2]
    monitorMetrics_id = sys.argv[3]
    monitorMetrics_name = sys.argv[4]
    log_init(log_file)
    mymonitor = myMonitor(log_file, last_id, monitorObj_id, monitorMetrics_id, monitorMetrics_name)
    mymonitor.start()
