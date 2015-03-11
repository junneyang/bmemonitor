#!/usr/bin/env python
#-*- coding: utf-8 -*-
import sys
import time
import datetime
import traceback

sys.path.append('../')
from com.logLib import *
from com.confLib import *
from com.cmdLib import *
from com.mysqlLib import *
from com.msgSend import *
from com.mailLib import *

class Monitor(object):
    def __init__(self, log_file, last_id, monitorObj_id, monitorMetrics_id, monitorMetrics_name):
        try:
            log_init(log_file)
            self.last_id = last_id
            self.monitorObj_id = monitorObj_id
            self.monitorMetrics_id = monitorMetrics_id
            self.monitorMetrics_name = monitorMetrics_name
            self.data = {}
            self.task_runner_conf = parse_conf("../conf/taskRunner.conf")
            self.subject = self.task_runner_conf['subject']
            self.mail_server  = self.task_runner_conf['mail_server']
            self.from_mail_addr  = self.task_runner_conf['from_mail_addr']
            self.to_mail_addr  = self.task_runner_conf['to_mail_addr']
            self.phone_list  = self.task_runner_conf['phone_list']
            self._debugmode = False
            logging.info("Monitor init success")
        except Exception as e:
            logging.error(str(e))


    # modfy debugmode
    def setDebug(self, debugMode):
        self._debugmode = debugMode

    #短信通知
    def msgSend(self, phone_list, content , mode="qapi"):
        msgSend(phone_list, content , mode="qapi")
    #邮件通知
    def mail_send(self, subject, content, from_mail_addr, to_mail_addr, mail_server):
        maillib = mailLib()
        maillib.simple_text_mail_send(subject, content, from_mail_addr, to_mail_addr, mail_server)
    #更新任务状态
    def update_task_status(self, task_id, status):
        try:
            mysql = mysqlLib()
            param=(status, task_id)
            mysql.update_tbl_monitortask_status(param)
            mysql.close()
            logging.info("task  task_id:" + str(task_id) + " database status modified to :" + str(status))
        except Exception as e:
            logging.error(str(e))
    #回填任务开始时间, starttime获取：cutime=datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")
    def update_task_starttime(self, task_id, starttime):
        try:
            mysql = mysqlLib()
            param=(starttime, task_id)
            mysql.update_tbl_monitortask_starttime(param)
            mysql.close()
            logging.info("task  task_id:" + str(task_id) + " database starttime update success")
        except Exception as e:
            logging.error(str(e))
    #回填任务结束时间
    def update_task_endtime(self, task_id, endtime):
        try:
            mysql = mysqlLib()
            param=(endtime, task_id)
            mysql.update_tbl_monitortask_endtime(param)
            mysql.close()
            logging.info("task  task_id:" + str(task_id) + " database endtime update success")
        except Exception as e:
            logging.error(str(e))
    #回填监控数据
    def add_monitor_data(self, task_id, status, info):
        try:
            mysql = mysqlLib()
            param=(task_id, status, json.dumps(info))
            n,last_id = mysql.add_tbl_monitordata(param)
            mysql.close()
            logging.info("add  monitor data last_id:" + str(last_id) + " to database success")
        except Exception as e:
            logging.error(str(e))
    #查询告警配置
    def query_alarm_conf(self, monitorObj_id, monitorMetrics_id):
        try:
            mysql = mysqlLib()
            param={"monitorObj_id":monitorObj_id,"monitorMetrics_id":monitorMetrics_id}
            retList = mysql.query_tbl_alarmconf(param)
            mysql.close()
            alarm_conf_id = int(retList[0][0])
            monitorObj_id = int(retList[0][1])
            monitorMetrics_id = int(retList[0][2])
            name = str(retList[0][3])
            description = str(retList[0][4])
            status = int(retList[0][5])
            conf =  json.loads(retList[0][6])
            logging.info("query  alarm conf monitorObj_id:" + str(monitorObj_id) + ",monitorMetrics_id:" +  str(monitorMetrics_id) +" success")
            return alarm_conf_id,monitorObj_id,monitorMetrics_id,name,description,status,conf
        except Exception as e:
            logging.error(str(e))
    #告警上报，注意代码逻辑：有的告警已经存在，继续上报，有的告警存在，不重复上报
    def add_alarm(self, alarmConf_id, monitorTask_id, monitorObj_id, monitorMetrics_id, description,status, datetime):
        try:
            mysql = mysqlLib()
            param=(alarmConf_id, monitorTask_id, monitorObj_id, monitorMetrics_id, description, status, datetime)
            n,last_id = mysql.add_alarmobj(param)
            mysql.close()
            logging.info("alarm object last_id:" + str(last_id) + " added success")
        except Exception as e:
            logging.error(str(e))
    #获取监控数据、上报告警等，此部分由具体子类改写实现。
    def monitor_alarm_proc(self):
        logging.info("task  task_id:" + str(self.last_id) + " monitor_alarm_proc start")
        self.data = {"datetime":"2015-01-11","data":888}
        self.add_monitor_data(self.last_id, 0, self.data)
        time.sleep(3)
        logging.info("task  task_id:" + str(self.last_id) + " monitor_alarm_proc end")
    #开始获取监控过程
    def start(self):
        try:
            #任务状态更新为执行中
            self.update_task_status(self.last_id, 3)
            #回填任务开始时间
            cutime=datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")
            self.update_task_starttime(self.last_id, cutime)
            #调用monitor_alarm_proc,获取监控数据、上报告警等
            self.monitor_alarm_proc()
            #任务状态更新为成功
            self.update_task_status(self.last_id, 4)
        except Exception as e:
            logging.error(str(e), exc_info=1)
            #任务状态更新为异常
            self.update_task_status(self.last_id, 5)
            msg = str(self.last_id) + "-" + str(self.monitorObj_id) + "-" + str(self.monitorMetrics_id) + "-" + str(self.monitorMetrics_name) + " task execute exception, please check it"
            self.msgSend(self.phone_list, msg , mode="qapi")
        finally:
            #任务完成时间回填
            cutime=datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")
            self.update_task_endtime(self.last_id, cutime)

if __name__ == "__main__":
    log_file = "./log/" + sys.argv[0] + ".log"
    last_id = sys.argv[1]
    monitorObj_id = sys.argv[2]
    monitorMetrics_id = sys.argv[3]
    monitorMetrics_name = sys.argv[4]
    monitor = Monitor(log_file, last_id, monitorObj_id, monitorMetrics_id, monitorMetrics_name)
    monitor.start()
