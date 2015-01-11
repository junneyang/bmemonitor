#!/usr/bin/env python
#-*- coding: utf-8 -*-
import sys
import time

sys.path.append('../')
from com.logLib import *
from com.confLib import *
from com.cmdLib import *
from Monitor import Monitor

class myMonitor(Monitor):
    #获取监控数据、上报告警等，此部分由具体子类改写实现。
    def monitor_alarm_proc(self):
        logging.info("task  task_id:" + str(self.last_id) + " monitor_alarm_proc start")
        #监控数据上报
        self.data = {"datetime":"2015-01-11","data":888}
        self.add_monitor_data(self.last_id, 0, self.data)
        time.sleep(3)
        logging.info("task  task_id:" + str(self.last_id) + " monitor_alarm_proc end")

if __name__ == "__main__":
    log_file = "./log/" + sys.argv[0] + ".log"
    last_id = sys.argv[1]
    monitorObj_id = sys.argv[2]
    monitorMetrics_id = sys.argv[3]
    monitorMetrics_name = sys.argv[4]
    log_init(log_file)
    mymonitor = myMonitor(log_file, last_id, monitorObj_id, monitorMetrics_id, monitorMetrics_name)
    mymonitor.start()
