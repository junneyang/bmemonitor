# !/usr/bin/env python
# -*- coding: UTF-8 -*-

################################################################################
#
# Copyright (c) 2015 Baidu.com, Inc. All Rights Reserved
#
#################################################################################
"""
BME Wise aladdin 页面监控：附近团购

Authors: chengyunlai@baidu.com
Date:    2015/03/08 23:55:06
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
# 监控类
# ------------------------------------------------------------------------------

class Wisealaddin_Monitor_Nearby(Monitor.Monitor):
    """Wise aladdin页面监控： 附近团购"""
    
    def __init__(self, log_file, last_id, monitorObj_id, monitorMetrics_id, monitorMetrics_name):
        Monitor.Monitor.__init__(self, log_file, last_id, monitorObj_id, monitorMetrics_id, monitorMetrics_name)
	self._job_nickname = "Wisealaddin_Monitor_Nearby"
    
    def monitor_alarm_proc(self):
    	"""Wise阿拉丁页面监控：附近团购卡片 业务逻辑实现类：
    		1) 获取卡片展现页面
    		2) 检查页面内容合法性
    		3) 保存获取的数据
    		4) 通知和报警
    	"""
        logging.info("[%s] task_id: %s monitor_alarm_proc start" % (self._job_nickname, self.last_id))
        pass
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
