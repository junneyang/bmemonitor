#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import json
import time

import gearman

sys.path.append('../..')
from com.logLib import *
from com.confLib import *
from com.cmdLib import *
from com.msgSend import *

reload(sys)
sys.setdefaultencoding("utf-8")

def gearwork(gearman_worker, gearman_job):
    params = {"RET":"gearwork INTERNAL ERROR"}
    taskrunner = None
    try:
        params = json.loads(gearman_job.data)
        logging.info("recv data : " + gearman_job.data)
        last_id = params['last_id']
        monitorObj_id = params['monitorObj_id']
        monitorMetrics_id = params['monitorMetrics_id']
        monitorMetrics_name = params['monitorMetrics_name']
        taskrunner = params['taskrunner']
        cmdstr = "cd ../../scripts && " + taskrunner + " " + str(last_id) + " " + str(monitorObj_id) + " " + str(monitorMetrics_id) + " " + str(monitorMetrics_name)
        #print cmdstr
        status,output = cmd_execute(cmdstr)
        logging.info(cmdstr + " executed success")
        logging.info("status: " + str(status))
        logging.info("output: " + str(output))
        if(int(status) != 0):
            raise Exception(str(output))
    except Exception as e:
        logging.error(taskrunner + str(e))
        conf = parse_conf("./conf/gearwork.conf")
        phone_list = conf['phone_list']
        msgSend(phone_list, u'【告警】gearwork dispatch exception : ' + taskrunner + str(e), mode="qapi")
    finally:
        logging.info("ret data : " + json.dumps(params))
        return json.dumps(params)

if __name__ == '__main__':
    try:
        conf = parse_conf("./conf/gearwork.conf")
        server_list = conf['server_list']
        log_file = conf['log_file']
        jobname = conf['jobname']
        log_init(log_file)
        worker = gearman.GearmanWorker(server_list)
        worker.register_task(str(jobname), gearwork)
        worker.work()
    except Exception as e:
        logging.error(str(e))
