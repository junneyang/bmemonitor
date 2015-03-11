# !/usr/bin/env python
# -*- coding: UTF-8 -*-

################################################################################
#
# Copyright (c) 2015 Baidu.com, Inc. All Rights Reserved
#
#################################################################################
"""
BME SEM 账户余额监控

Authors: chengyunlai@baidu.com
Date:    2015/03/06 20:55:06
"""

import copy
import datetime
import logging
import os
import time
import traceback
import sys

import torndb

import Monitor

BASE_PATH = os.getcwd()
sys.path.append(BASE_PATH + "/../")

import com.msgSend as MsgUtil
from com.logLib import *



# ------------------------------------------------------------------------------
# 账户信息获取
# ------------------------------------------------------------------------------
SEM_API_PATH = os.path.dirname(os.path.realpath(__file__)) + "/semapi/"
sys.path.append(SEM_API_PATH)

from sms_v3_AccountService import *

class Sem_AccountInfo(object):
    """账户信息，名称，api授权码，cid
    """
    # 账户信息获取数据库连接配置
    ACCOUNT_DB_CONF = { # mysql -ubmeqa -pbmeqa123 -h10.94.54.51 -P8456
        "host" 			: 	"10.94.54.51:8456",
        "db" 			: 	"monitor",
        "time_zone" 	        : 	"+8:00",
        "user" 			: 	"bmeqa",
        "password" 		: 	"bmeqa123",
    }

    # API重试次数
    API_RETRY_TIME = 5

    def __init__(self):
        self.accountId      = 0         # id
        self.accountName    = ""        # 账户名称
        self.accountPwd     = ""        # 账户密码
        self.appid          = ""        # api访问的授权码
        self.cid            = []        # 账户配置的天兔cid
        self.isActive       = 0         # 状态
        self.balance        = -2 
 
    def __str__(self):
        strTpl = "Id = {0}, Name = {1}, Password = {2}, appid = {3}, cid = {4}, isActive = {5}"
        return strTpl.format(self.accountId, self.accountName, self.accountPwd,
                    self.appid, str(self.cid), self.isActive)

    def getBalance(self):
        """获取账户余额信息
        """
        os.chdir(SEM_API_PATH)

        retrys = 0  # 保存重试次数
        
        accountSvr = sms_v3_AccountService()
        accountSvr.setUsername(self.accountName)
        accountSvr.setPassword(self.accountPwd)
        accountSvr.setToken(self.appid)
        #print accountSvr
        #print self
        balance = -2
        while retrys < Sem_AccountInfo.API_RETRY_TIME:
            try:
                balanceInfo = accountSvr.getAccountInfo()
                #print balanceInfo
                logging.info(str(balanceInfo))
                balance = balanceInfo['body']['accountInfoType']['balance']
                break   			# 获取成功，则退出循环
            except Exception as err:
                logging.error(traceback.format_exc())
                balance = -1   		# api获取失败，设置-1
                time.sleep(5)
            finally:
                retrys += 1
        
        self.balance = balance
        os.chdir(BASE_PATH)

        return balance
 
    @classmethod
    def loadsFromdb(cls):
        """从数据库读取账户信息
        """
        dbConf = copy.deepcopy(cls.ACCOUNT_DB_CONF)
        host = dbConf['host']
        db = dbConf['db']
        del dbConf['host']
        del dbConf['db']

        cnt = torndb.Connection(host, db, **dbConf)
        sql = "select * from accountInfo where isActive = 1"
        ret = cnt.query(sql)
        cnt.close()

        accountList = []
        for record in ret:
            at = Sem_AccountInfo()
            at.accountId = record['accountId']
            at.accountName = record['accountName'].encode("utf8")
            at.accountPwd = record['pwd'].encode("utf8")
            at.appid = record['appid'].encode("utf8")
            at.cid = record['cid'].encode("utf8").split("/")
            at.isActive = record['isActive']
            accountList.append(at)
        return accountList

# ------------------------------------------------------------------------------
# Sem 消息通知辅助类
# ------------------------------------------------------------------------------

class Sem_MessageHelper(object):
    """消息处理
    """
    
    # ------------- 邮件格式设置 --------------------
    # 邮件内容模板
    TPL_LETTER = ('<!DOCTYPE html><!--STATUS OK--><html><head>'
        '<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">'
        '<meta http-equiv="content-type" content="text/html;charset=gb2312">'
        '<style>{tableStyle}</style></head>'
        '<body><table border = "1" cellpadding="3" cellspacing="0">'
        '{itemRows}</table></body></html>')
    # 余额报表表头模板
    TPL_ROW_ITEM_HEADER = '''<tr><td>序号</td><td>账户名</td><td>时间</td><td>账户余额(元)</td></tr>'''
    # 余额报表数据行模板
    TPL_ROW_ITEM = '''<tr><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td></tr>'''
    # 邮件发送者
    EMAIL_FROM = "bme-monitor@baidu.com"
    # 邮件主题
    EMAIL_SUBJECT = "[Bme监控][SEM账户余额报告]"
    # 邮件接收人列表
    EMAIL_RECIEVER = ['yangjun03','yanhuawei','wangyuhan','chengyunlai','wangzhichao04']

    # ------------- 短信格式设置 ----------------------
    # 常规通知格式
    GSM_TPL_NOTIFY = "本次监控账户余额是 {0} 至 {1} 之间. "
    # 错误通知格式
    GSM_TPL_ERROR  = "共 {0} 个账户获取余额失败, {1} ..."
    # 短信接收人
    GSM_RECIEVER = {
    	"18810603945" : "qa, chengyunlai",
    	"18511870304" : "pm, wangyuhan",
    	"15810634448" : "rd, wangzhichao04",
    }

    def __init__(self, jobTime = None):
        if jobTime is not None: self._jobTime = jobTime
        else: self._jobTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') 

    def makeEmailContext(self, accounts):
        """生成邮件内容

        Args：
        	accounts: Sem_AccountInfo列表对象，已经计算过balance信息

        Returns:
        	本批次监控账户余额报表，html

        """
        itemRows = []
        itemRows.append(Sem_MessageHelper.TPL_ROW_ITEM_HEADER)
        #print type(itemRows)

        # 拼接单个账户的余额
        for aid in range(len(accounts)):
            ac = accounts[aid]
            itemStr = Sem_MessageHelper.TPL_ROW_ITEM.format(aid + 1, ac.accountName, 
            	self._jobTime, ac.balance)
            itemRows.append(itemStr)
        
        # 生成余额报表，设置表格css样式
        return Sem_MessageHelper.TPL_LETTER.format(**{
                'itemRows' : "".join(itemRows),
                'tableStyle': """table{border-collapse:collapse;border-spacing:0;border:1px solid #888;} 
                                 th,td{border:1px solid #888;padding:5px 15px;}
                                 th{font-weight:bold;background:#ccc;}""",
        })

    def makeGsmContent(self, accounts):
        """生成短信内容

        Args：
        	accounts: Sem_AccountInfo列表对象，已经计算过balance信息

        Returns:
        	二元组，(错误数量，短信通知报警信息)

        """
        errList = []		# 获取余额信息错误的，-1异常，-2初始值
        succList = []		# 获取余额信息成功的，>=0

        for ac in accounts:
            if ac.balance < 0: errList.append(ac.accountName)
            else: succList.append(ac.balance)

        errCount = len(errList)
        gsmContent = "[闪投账户余额] "

        if len(succList) > 0:
            gsmContent += Sem_MessageHelper.GSM_TPL_NOTIFY.format(min(succList), max(succList)) 

        if errCount > 0:
            gsmContent += Sem_MessageHelper.GSM_TPL_ERROR.format(errCount, errList[0])

        return errCount, gsmContent

    def sendEmail(self, emailContent, debugMode = False):
        """发送邮件

        Args：
        	emailContent: 邮件内容，html格式
        	debugMode: 是否开启debug模式，默认为False

        Returns: 
        	None. debugMode = True, 发送邮件到邮件到chengyunlai@baidu.com;
                      debugMode = False, 发送邮件到邮件到配置的接收人

        """
        sendCommand = ("echo '{emailCtx}'|/usr/bin/formail -I \"From: {emailFrom}\""
                    " -I \"MIME-Version:1.0\" -I \"Content-type:text/html;charset=gb2312\""
                    " -I \"Subject: {emailSubject}\" -I \"To: {emailTo}\""
                    "|/usr/sbin/sendmail -oi {emailTo}")
        commandParams = { 
            'emailCtx': emailContent.decode("utf8").encode('gbk'),
            'emailFrom': Sem_MessageHelper.EMAIL_FROM,
            'emailSubject': Sem_MessageHelper.EMAIL_SUBJECT.decode("utf8").encode("gbk"), 
            'emailTo': " ".join([ x + "@baidu.com" for x in Sem_MessageHelper.EMAIL_RECIEVER]),
        }

        if debugMode: commandParams['emailTo'] = "chengyunlai@baidu.com"
        os.popen(sendCommand.format( **commandParams ))        

    def sendGSM(self, gsmContent, debugMode = False):
        """发送短信

        Args：
        	gsmContent: 短信内容，UTF-8编码
        	debugMode: 是否开启debug模式，默认为False

        Returns: 
        	None. debugMode = True, 发送短信到 18810603945;
        	      debugMode = False, 发送到配置的接收人

        """
        gsmReciver = ['18810603945'] if debugMode else Sem_MessageHelper.GSM_RECIEVER.keys()
        MsgUtil.msgSend(gsmReciver, gsmContent, "qapi")
       	pass
pass



# ------------------------------------------------------------------------------
# 监控类
# ------------------------------------------------------------------------------

class Sem_Monitor_Balance(Monitor.Monitor):
    """SEM 账户余额监控"""
    
    def __init__(self, log_file, last_id, monitorObj_id, monitorMetrics_id, monitorMetrics_name):
        Monitor.Monitor.__init__(self, log_file, last_id, monitorObj_id, monitorMetrics_id, monitorMetrics_name)
        self._job_nickname = "SEM_Balance_Monitor"
    
    def monitor_alarm_proc(self):
    	"""SEM 账户余额监控 业务逻辑实现类：
    		1) 从数据库读取账户信息；
    		2) 从闪投API获取账户余额；
    		3) 保存获取的数据；
    		4) 通知和报警；
    	"""
        logging.info("[%s] task_id: %s monitor_alarm_proc start" % (self._job_nickname, self.last_id))

        # 1) 从数据库读取账户信息；
        semAccountList = Sem_AccountInfo.loadsFromdb()
        logging.info("[%s] task_id: %s load account from db end: %d " % (self._job_nickname, self.last_id, len(semAccountList)))
        
        # 2) 从闪投API获取账户余额
        semMsgHelper = Sem_MessageHelper()
        for account in semAccountList: account.getBalance()
        logging.info("[%s] task_id: %s get all balance end" % (self._job_nickname, self.last_id))
        
        # 3) 保存获取的数据
        balanceSaveList = [ { "balance": ac.balance, 
                              "datetime": semMsgHelper._jobTime, 
                              "accountName": ac.accountName,
                            } for ac in semAccountList ]
        self.add_monitor_data(self.last_id, 0, balanceSaveList)
        logging.info("[%s] task_id: %s save balance to tbl_monitordata end" % (self._job_nickname, self.last_id))
        
        # 4) 通知和报警
        errCount, gsmContent = semMsgHelper.makeGsmContent(semAccountList)
        emailContent = semMsgHelper.makeEmailContext(semAccountList)
        logging.info("[%s] task_id: %s error count = %d" % (self._job_nickname, self.last_id, errCount))
        
        if self._debugmode:  # 调试模式
            semMsgHelper.sendEmail(emailContent, True)
            semMsgHelper.sendGSM(gsmContent, True)
        
        # alarm_conf_id,monitorObj_id,monitorMetrics_id,name,description,status,conf
        alarmCfg = self.query_alarm_conf(self.monitorObj_id, self.monitorMetrics_id)	
        alarmdescList = []
        # 报警策略
        if errCount >= 8:  		# 出现异常立即报警
            alarmdescList.append("{0}: {1}个账户从api获取余额失败!".format(alarmCfg[4], errCount))
        # 计算平均值, 如果小于阈值报警
        balanceNumList = [ ac.balance for ac in semAccountList if ac.balance >= 0 ]
        balanceavg =  1.0 * sum(balanceNumList) / len(balanceNumList) if balanceNumList else 0
        if balanceavg < 5000000: 
            alarmdescList.append("{0}: 余额{1}不足500W,请尽快充值！".format(alarmCfg[4], balanceavg))
        
        hourInt = int(datetime.datetime.now().strftime('%H'))
        # 设置通知时间段
        if balanceavg > 9000000:        #余额大于900W，每天通知一次,上午10点钟
            hourNotifyList = [10]
        elif balanceavg > 5000000:      #余额大于500W，每天通知3次，10、18、0点
            hourNotifyList = [10, 18, 0]
        else:
            hourNotifyList = [8, 10, 12, 18, 20, 0]

        logging.info("[%s] task_id: %s , avg(balance) = %f, hourNotifyList = %s" % (self._job_nickname, self.last_id, balanceavg, str(hourNotifyList)))
        
        # notify to db
        currTime = datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")
        logging.info("[%s] task_id: %s alarm count = %d" % (self._job_nickname, self.last_id, len(alarmdescList)))
        
        for alarmdesc in alarmdescList:
            logging.info("[%s] task_id: %s alarm message: %s" % (self._job_nickname, self.last_id, alarmdesc))
            self.add_alarm(alarmCfg[0], self.last_id, alarmCfg[1],alarmCfg[2], alarmdesc , 0, currTime)
        if errCount >= 8 or hourInt in hourNotifyList:
            semMsgHelper.sendGSM(gsmContent, self._debugmode)
            semMsgHelper.sendEmail(emailContent, self._debugmode)
        
        logging.info("[%s] task_id: %s monitor_alarm_proc end" % (self._job_nickname, self.last_id))

pass

## for test
def testSelf():
    log_file = "./log/sem_monitor_balance_test.log"
    last_id = 17390
    monitorObj_id = 3
    monitorMetrics_id = 1
    monitorMetrics_name = "账户余额"
    log_init(log_file)
    
    mymonitor = Sem_Monitor_Balance(log_file, last_id, monitorObj_id, monitorMetrics_id, monitorMetrics_name)
    mymonitor.setDebug(True)
    mymonitor.phone_list = ["18810603945"]
    mymonitor.start()

#testSelf()
#exit()
## Start up for bme_sem_monitor_balance
if __name__ == "__main__":
    log_file = "./log/" + sys.argv[0] + ".log"
    last_id = sys.argv[1]
    monitorObj_id = sys.argv[2]
    monitorMetrics_id = sys.argv[3]
    monitorMetrics_name = sys.argv[4]
    log_init(log_file)
    
    mymonitor = Sem_Monitor_Balance(log_file, last_id, monitorObj_id, monitorMetrics_id, monitorMetrics_name)
    mymonitor.start()
