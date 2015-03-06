#!/usr/bin/env python
#-*- coding: utf-8 -*-
import sys
import time
import datetime
import re
import threading
import multiprocessing
import traceback
import hashlib
import json

sys.path.append('../')
from com.logLib import *
from com.ftpLib import *
from com.cmdLib import *
from com.mysqlLib import *

'''#回填监控数据
def add_monitor_data(task_id, info):
    try:
        mysql = mysqlLib()
        param=(task_id, json.dumps(info))
        n,last_id = mysql.add_zhixin_monitordata()
        mysql.close()
        logging.info("add  monitor data last_id:" + str(last_id) + " to database success")
    except Exception as e:
        logging.error(str(e))'''

class zhixinDelayThread(multiprocessing.Process):
    def __init__(self, hostname, datetime, last_id):
        log_init("./log/zhixinDelayThread.log")
        multiprocessing.Process.__init__(self,name=hostname + datetime)
        self.hostname = hostname
        self.datetime = datetime
        self.last_id = last_id
        self.keystr_request = "zhixin New as params,"
        self.keystr_as_total = "zhixin New as response"
        self.keystr_as_cost = "new as cost"
        self.keystr_zhixin_total = "zhixin_show"
        self.keystr_zhixin_cost = "Zhixin Query request cost"
        self.log_stat = {}
    def run(self):
        #获取logid请求参数
        self.ftpPath = "ftp://" + self.hostname + "/home/tuan/odp/log/zhixin/zhixin.log." + self.datetime
        self.line_list = None
        try:
            self.line_list = geFtpFile2Memory(self.ftpPath, self.keystr_request)
        except Exception as e:
            logging.error("", exc_info=1)
            return
        for line in self.line_list:
            tmp_line_list = re.split("[][]", line)
            logid = tmp_line_list[5]
            req_param = tmp_line_list[22]
            req_param_list = req_param.split(",")
            try:
                city_id = req_param_list[1].split(":")[1]
                srcID = req_param_list[2].split(":")[1]
                keyword = req_param_list[3].split(":")[1]
                original_query = req_param_list[4].split(":")[1]
                req_type = req_param_list[5].split(":")[1]
                self.log_stat[logid] = {
                    "city_id":city_id,
                    "srcID":srcID,
                    #"keyword":keyword.decode('GBK').encode('UTF-8'),
                    #"original_query":original_query.decode('GBK').encode('UTF-8'),
                    #"req_type":req_type,
                    "as_null":0,
                    "as_delay":0,
                    "zhixin_null":0,
                    "zhixin_delay":0
                }
            except Exception as e:
                logging.error("line : " + line)
                logging.error("req_param : " + req_param)
                #traceback.print_exc()
                logging.error("", exc_info=1)

        '''#logid维度获取各项指标
        for logid in self.log_stat:
            self.line_list = geFtpFile2Memory(self.ftpPath, logid)
            for line in self.line_list:
                if(self.keystr_as_total in line):
                    tmp_line_list = re.split("zhixin New as response,total:", line)
                    as_total = int(tmp_line_list[1])
                    if(as_total == 0):
                        self.log_stat[logid]['as_null'] = 1
                elif(self.keystr_as_cost in line):
                    tmp_line_list = re.split("new as cost ", line)
                    as_delay = int(tmp_line_list[1].split(" ")[0])
                    self.log_stat[logid]['as_delay'] = as_delay
                elif(self.keystr_zhixin_total in line):
                    tmp_line_list = re.split("zhixin_show", line)
                    if(tmp_line_list[1] == "[]"):
                        self.log_stat[logid]['zhixin_null'] = 1
                elif(self.keystr_zhixin_cost in line):
                    tmp_line_list = re.split("Zhixin Query request cost ", line)
                    zhixin_delay = int(tmp_line_list[1].split(" ")[0])
                    self.log_stat[logid]['zhixin_delay'] = zhixin_delay'''

        #logid维度获取各项指标-as_null指标
        self.line_list = geFtpFile2Memory(self.ftpPath, self.keystr_as_total)
        for logid in self.log_stat:
            for line in self.line_list:
                if(logid in line):
                    tmp_line_list = re.split("zhixin New as response,total:", line)
                    try:
                        as_total = int(tmp_line_list[1])
                        if(as_total == 0):
                            self.log_stat[logid]['as_null'] = 1
                    except Exception as e:
                        logging.error(str(e), exc_info=1)
        #logid维度获取各项指标-as_delay指标
        self.line_list = geFtpFile2Memory(self.ftpPath, self.keystr_as_cost)
        for logid in self.log_stat:
            for line in self.line_list:
                if(logid in line):
                    tmp_line_list = re.split("new as cost ", line)
                    as_delay = int(tmp_line_list[1].split(" ")[0])
                    self.log_stat[logid]['as_delay'] = as_delay
        #logid维度获取各项指标-as_delay指标
        self.line_list = geFtpFile2Memory(self.ftpPath, self.keystr_zhixin_total)
        for logid in self.log_stat:
            for line in self.line_list:
                if(logid in line):
                    tmp_line_list = re.split("zhixin_show", line)
                    if(tmp_line_list[1] == "[]"):
                        self.log_stat[logid]['zhixin_null'] = 1
        #logid维度获取各项指标-as_delay指标
        self.line_list = geFtpFile2Memory(self.ftpPath, self.keystr_zhixin_cost)
        for logid in self.log_stat:
            for line in self.line_list:
                if(logid in line):
                    tmp_line_list = re.split("Zhixin Query request cost ", line)
                    zhixin_delay = int(tmp_line_list[1].split(" ")[0])
                    self.log_stat[logid]['zhixin_delay'] = zhixin_delay
        '''print self.log_stat
        total_len = 0
        for item in self.log_stat:
            total_len += 1
        print total_len'''

        #遍历log_stat, 给出最终hostname,date,cityID,srcID维度的统计数据——初始化
        tmp_stat = {}
        for item in self.log_stat:
            data = self.log_stat[item]
            tmp_key = self.hostname + self.datetime + data['city_id'] + data['srcID']
            md5_data = hashlib.md5(tmp_key.encode("utf-8")).hexdigest()
            tmp_stat[md5_data] = {
                "hostname":self.hostname,
                "datetime":self.datetime,
                "city_id":data['city_id'],
                "srcID":data['srcID'],
                "flow":0,
                "as_null":0,
                "as_delay":0,
                "zhixin_null":0,
                "zhixin_delay":0
            }
        #遍历log_stat, 给出最终hostname,date,cityID,srcID维度的统计数据——统计计算
        for item in self.log_stat:
            data = self.log_stat[item]
            tmp_key = self.hostname + self.datetime + data['city_id'] + data['srcID']
            md5_data = hashlib.md5(tmp_key.encode("utf-8")).hexdigest()
            tmp_stat[md5_data]['hostname'] = self.hostname
            tmp_stat[md5_data]['datetime'] = self.datetime
            tmp_stat[md5_data]['city_id'] = data['city_id']
            tmp_stat[md5_data]['srcID'] = data['srcID']
            tmp_stat[md5_data]['flow'] += 1
            tmp_stat[md5_data]['as_null'] += data['as_null']
            tmp_stat[md5_data]['as_delay'] += data['as_delay']
            tmp_stat[md5_data]['zhixin_null'] += data['zhixin_null']
            tmp_stat[md5_data]['zhixin_delay'] += data['zhixin_delay']
        #print tmp_stat
        #监控数据入库
        mysql = mysqlLib()
        for item in tmp_stat:
            try:
                hostname = tmp_stat[item]['hostname']
                date = tmp_stat[item]['datetime']
                a = time.strptime(date,'%Y%m%d%H')
                timestamp = time.mktime(a)
                localtime = time.localtime(timestamp)
                date = time.strftime('%Y-%m-%d %H:%M:%S',localtime)

                city_id = tmp_stat[item]['city_id']
                srcID = tmp_stat[item]['srcID']
                flow = tmp_stat[item]['flow']
                as_null = tmp_stat[item]['as_null']
                as_delay = tmp_stat[item]['as_delay']/float(flow)
                zhixin_null = tmp_stat[item]['zhixin_null']
                zhixin_delay = tmp_stat[item]['zhixin_delay']/float(flow)
                param=(self.last_id, hostname, date, city_id, srcID, flow, as_null, as_delay, zhixin_null, zhixin_delay,0)
                n,last_id = mysql.add_zhixin_monitordata(param)
            except Exception as e:
                logging.error(str(e), exc_info=1)
        mysql.close()


if __name__ == '__main__':
    hostname = "yf-tuangou-new-web00.yf01"
    datetime = "2015020212"
    #mutex=threading.Lock()
    zhixinDelayThread_th = zhixinDelayThread(hostname, datetime)
    zhixinDelayThread_th.start()
    zhixinDelayThread_th.join()
    #print stat

