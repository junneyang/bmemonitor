#!/usr/bin/env python
#-*- coding: utf-8 -*-
import sys
import json

from apscheduler.scheduler import Scheduler
import time
import datetime

from com.logLib import *
from com.confLib import *
from com.mysqlLib import *
from com.msgSend import *
from com.mailLib import *
from dispatch.gearclient.gearClient import *

class taskRunner():
    def __init__(self,task_conf):
        try:
            self.task_conf = parse_conf(task_conf)
            self.taskrunner_conf = parse_conf("./conf/taskRunner.conf")
            self.log_file = self.taskrunner_conf['log_file']
            self.subject = self.taskrunner_conf['subject']
            self.mail_server = self.taskrunner_conf['mail_server']
            self.from_mail_addr = self.taskrunner_conf['from_mail_addr']
            self.to_mail_addr = self.taskrunner_conf['to_mail_addr']
            self.phone_list = self.taskrunner_conf['phone_list']
            self.jobname = self.taskrunner_conf['jobname']
            log_init(self.log_file)
            logging.info("taskRunner init success")
        except Exception as e:
            logging.error(str(e))
    #查询监控指标
    def get_monitorMetrics(self, monitorMetrics_id):
        try:
            mysql = mysqlLib()
            param={"id":monitorMetrics_id}
            retList = mysql.query_monitormetrics(param)
            mysql.close()
            ret_monitorMetrics_id = int(retList[0][0])
            ret_monitorObj_id = int(retList[0][1])
            ret_monitorMetrics_name = retList[0][2]
            logging.info("get_monitorMetrics : " + str(monitorMetrics_id) + ", success")
            return ret_monitorMetrics_id,ret_monitorObj_id,ret_monitorMetrics_name
        except Exception as e:
            logging.error(str(e))
    #更新任务状态
    def update_task_status(self, task_id, status):
        mysql = mysqlLib()
        param=(status, task_id)
        mysql.update_tbl_monitortask_status(param)
        mysql.close()
        logging.info("task  task_id:" + str(task_id) + " database status modified to :" + str(status))
    #任务入库
    def add_job(self, monitorObj_id, monitorMetrics_id, monitorMetrics_name, taskrunner):
        try:
            mysql = mysqlLib()
            param=(monitorObj_id, monitorMetrics_id, 0)
            n,last_id = mysql.add_task(param)
            mysql.close()
            logging.info("add_job  last_id:" + str(last_id) + ",monitorObj_id:" + str(monitorObj_id) + ",monitorMetrics_id:" + str(monitorMetrics_id) + " to database success")

            jobname = self.jobname
            jobparameters = {"last_id":last_id,"monitorObj_id":monitorObj_id,"monitorMetrics_id":monitorMetrics_id,"monitorMetrics_name":monitorMetrics_name,"taskrunner":taskrunner}
            gearclient = gearClient()
            gearclient.job_submit(str(jobname), jobparameters, wait_until_complete = False, background = True)
            logging.info("gear job  last_id:" + str(last_id) + ",monitorObj_id:" + str(monitorObj_id) + ",monitorMetrics_id:" + str(monitorMetrics_id) + " submited success")
            self.update_task_status(last_id, 1)
        except Exception as e:
            logging.error(str(e))
    #根据配置文件提交任务
    def tasksubmit(self):
        try:
            for item in self.task_conf:
                #获取监控对象、监控指标
                monitorObj_id = item['monitorObj_id']
                monitorMetrics_id = item['monitorMetrics_id']
                monitorMetrics_name = item['monitorMetrics_name']
                taskrunner = item['taskrunner']

                #status为1表示有效监控，否则视为下架
                if(item['status'] == 1):
                    ret_monitorMetrics_id,ret_monitorObj_id,ret_monitorMetrics_name = self.get_monitorMetrics(monitorMetrics_id)
                    try:
                        assert(monitorObj_id == ret_monitorObj_id)
                        assert(monitorMetrics_id == ret_monitorMetrics_id)
                        assert(monitorMetrics_name == ret_monitorMetrics_name)
                        info_str = str(monitorObj_id) + "," + str(monitorMetrics_id) + "," + monitorMetrics_name + "verify success"
                        logging.info(info_str)
                    except Exception as e:
                        #校验异常，打日志，发短信、邮件通知系统管理员
                        error_str = u"taskRunner.conf 任务配置有误 ：" + str(monitorObj_id) + "," + str(monitorMetrics_id) + ","
                        + monitorMetrics_name + u" 合法性校验失败，请检查此任务配置"
                        logging.error(error_str)
                        logging.error(str(e))
                        #短信通知
                        msgSend(self.phone_list, self.subject + " : " + error_str, mode="qapi")
                        #邮件通知
                        maillib = mailLib()
                        maillib.simple_text_mail_send(self.subject, error_str, self.from_mail_addr, self.to_mail_addr, self.mail_server)
                        continue

                    #校验通过，根据start_type提交合适的任务
                    #---------------------------------------------------------------------------------------------
                    #任务类型
                    # 0：定时启动，此时需要配置定时启动时间、间隔时间；
                    # 1：间隔启动，此时需要配置间隔周期；
                    # 2: 立即启动，一次性任务
                    #---------------------------------------------------------------------------------------------
                    start_type = item['start_type']
                    #类型：定时提交
                    if(start_type == 0):
                        start_time = item['start_time']
                        period = item['period']
                        sched = Scheduler()
                        sched.daemonic = False
                        dd = datetime.datetime.now()
                        dd_delta = dd + datetime.timedelta(days=0)
                        cutime=dd_delta.strftime("%Y-%m-%d")
                        ddnew_str = cutime + " " + start_time
                        ddnew = datetime.datetime.fromtimestamp(time.mktime(time.strptime(ddnew_str, "%Y-%m-%d %H:%M:%S")))
                        sched.add_interval_job(self.add_job, minutes=period, start_date=ddnew, args=[monitorObj_id, monitorMetrics_id, monitorMetrics_name, taskrunner])
                        sched.start()
                        logging.info("add_interval_job success")

                    #类型：间隔提交
                    elif(start_type == 1):
                        period = item['period']
                        sched = Scheduler()
                        sched.daemonic = False
                        sched.add_cron_job(self.add_job, minute='*/' + str(period), args=[monitorObj_id, monitorMetrics_id, monitorMetrics_name, taskrunner])
                        sched.start()
                        logging.info("add_cron_job success")
                    #类型：立即
                    elif(start_type == 2):
                        self.add_job(monitorObj_id, monitorMetrics_id, monitorMetrics_name, taskrunner)
                        logging.info("add instant job success")
        except Exception as e:
            logging.error(str(e))

if __name__ == "__main__":
    if(len(sys.argv) != 2):
        print("""======================================================================================
|                              Usage Instructions                                    |
======================================================================================""")
        print("""|  usage              : python taskRunner.py taskConf""")
        print("""|  example            : python taskRunner.py ./conf/period_task.conf""")
        print("""======================================================================================""")
        sys.exit()
    taskConf = sys.argv[1]
    taskrunner = taskRunner(taskConf)
    taskrunner.tasksubmit()

