#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import json

import gearman

sys.path.append('../..')
from com.logLib import *
from com.confLib import *

class gearClient(object):
    def __init__(self):
        try:
            self.conf = parse_conf("./conf/gearclient.conf")
            self.server_list = self.conf['server_list']
            self.log_file = self.conf['log_file']
            log_init(self.log_file)
            self.gm_client = gearman.GearmanClient(self.server_list)
        except Exception as e:
            logging.error(str(e))

    #---------------------------------------------------------------------------------------------
    #wait_until_complete = True，background = True     : jobclient提交任务，收到jobserver确认消息之后，断开与server连接，client进程结束(CREATED,None)
    #wait_until_complete = True，background = False    : jobclient与jobserver一直保持连接，client进程阻塞等待server返回结果(COMPLETE,{"a": 123, "b": 321})
    #wait_until_complete = False，background = True    : jobclient提交任务，收到jobserver确认消息之后，断开与server连接，client进程结束(CREATED,None)
    #wait_until_complete = False，background = False   : jobclient与jobserver一直保持连接，jobclient可继续抓取任务状态(CREATED,None)——(CREATED,None)
    #---------------------------------------------------------------------------------------------
    def job_submit(self, jobname, jobparameters, wait_until_complete = True, background = True):
        try:
            params = json.dumps(jobparameters)
            submitted_job_request = self.gm_client.submit_job(jobname, params, wait_until_complete = wait_until_complete, background = background)
            #print submitted_job_request.state
            #print submitted_job_request.result
        except Exception as e:
            logging.error(str(e))

if __name__ == '__main__':
    jobname = "gearwork"
    jobparameters = {"a":123,"b":321}
    gearclient = gearClient()
    gearclient.job_submit(jobname, jobparameters, wait_until_complete = False, background = True)
