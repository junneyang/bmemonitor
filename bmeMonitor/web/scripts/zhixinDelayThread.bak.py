#!/usr/bin/env python
#-*- coding: utf-8 -*-
import sys
import time
import datetime
import re
import threading
import traceback
import hashlib

sys.path.append('../')
from com.logLib import *
from com.ftpLib import *
from com.cmdLib import *

class zhixinDelayThread(threading.Thread):
    def __init__(self, hostname, datetime):
        log_init("./log/zhixinDelayThread.log")
        threading.Thread.__init__(self,name=hostname + datetime)
        self.hostname = hostname
        self.datetime = datetime
        self.keystr_request = "zhixin New as params,"
        self.keystr_total = "New as response,total:"
        self.tmp_data = {}
        self.tmp_stat = {}
    def run(self):
        ftpPath = "ftp://" + self.hostname + "/home/tuan/odp/log/zhixin/zhixin.log." + self.datetime
        fp = geFtpFile2Memory(ftpPath)
        for line in fp:
            line = line.strip()
            if(self.keystr_request in line):
                line_list = re.split("[][]", line)
                req_time = line_list[0].split(" ")[1] + " " + line_list[0].split(" ")[2]
                logid = line_list[5]
                req_param = line_list[22]
                try:
                    req_param_list = req_param.split(",")
                    city_id = req_param_list[1].split(":")[1]
                    srcID = req_param_list[2].split(":")[1]
                    keyword = req_param_list[3].split(":")[1]
                    original_query = req_param_list[4].split(":")[1]
                    req_type = req_param_list[5].split(":")[1]
                    #print req_time,logid,city_id,srcID,keyword,original_query,req_type
                    key_data = self.hostname + self.datetime + logid
                    md5_data = hashlib.md5(key_data.encode("utf-8")).hexdigest()
                    data = {
                        "hostname":hostname,
                        "datetime":datetime,
                        "logid":logid,
                        "city_id":city_id,
                        "srcID":srcID,
                        "keyword":keyword.decode('GBK').encode('UTF-8'),
                        "original_query":original_query.decode('GBK').encode('UTF-8'),
                        "req_type":req_type
                    }
                    self.tmp_data[md5_data] = data
                    '''if mutex.acquire():
                        self.tmp[md5_data] = data
                    mutex.release()'''
                except Exception as e:
                    logging.error("line : " + line)
                    logging.error("req_param : " + req_param)
                    #traceback.print_exc()
                    logging.error("", exc_info=1)


        print self.tmp_data
        print len(self.tmp_data)

if __name__ == '__main__':
    hostname = "yf-tuangou-new-web00.yf01"
    datetime = "2015020212"
    stat = {}
    mutex=threading.Lock()
    zhixinDelayThread_th = zhixinDelayThread(hostname, datetime)
    zhixinDelayThread_th.start()
    zhixinDelayThread_th.join()
    #print stat

