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

reload(sys)
sys.setdefaultencoding( "utf-8" )

def gearwork(gearman_worker, gearman_job):
    params = {"RET":"gearwork INTERNAL ERROR"}
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
        cmd_execute(cmdstr)
        logging.info(cmdstr + " executed success")
    except Exception as e:
        logging.error(str(e))
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
