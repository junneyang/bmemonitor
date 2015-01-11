#!/usr/bin/env python
#-*- coding: utf-8 -*-
from apscheduler.scheduler import Scheduler
import time

# Start the scheduler
sched = Scheduler()


def job_function(str):
    print "Hello World, " + str

print 'start to sleep'
sched.daemonic = False
sched.add_cron_job(job_function,day_of_week='*', hour='*', minute='*',second='*/1', args=["junneyang"])
sched.start()


