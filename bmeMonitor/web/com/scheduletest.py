#-*-coding:utf-8-*-
from apscheduler.scheduler import Scheduler

def job_function(a):
    print a

if __name__ == '__main__':
    hello = 'hello world'
    sched = Scheduler(daemonic=False) # 注意这里，要设置 daemonic=False
    sched.add_cron_job(job_function, day_of_week='*', hour='*', minute='1', second='*', args=[hello]) # args=[] 用来给job函数传递参数
    sched.start()

