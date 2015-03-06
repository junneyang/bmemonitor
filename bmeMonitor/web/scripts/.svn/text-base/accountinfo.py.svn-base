#!/usr/bin/env python
#-*- coding: utf-8 -*-
import sys
import time
import datetime
import pickle
import MySQLdb

sys.path.append('../')
from com.logLib import *
host='10.94.54.51'
user='bmeqa'
passwd='bmeqa123'
db='monitor'
port=8456

reload(sys)
sys.setdefaultencoding( "utf-8" )

class AccountInfo():
    #--------------------------------------------------------------------------------------------------------
    #sql打开、关闭操作
    #--------------------------------------------------------------------------------------------------------
    def __init__(self,host=host,user=user,passwd=passwd,db=db,port=port,charset='utf8'):
        try:
            self.host=host
            self.user=user
            self.passwd=passwd
            self.db=db
            self.port=port
            self.charset=charset
            self.conn=MySQLdb.connect(host=self.host,user=self.user,passwd=self.passwd,db=self.db,port=self.port,charset=self.charset)
            self.cursor=self.conn.cursor()
            logging.info("INFO, connect success")
        except Exception as e:
            logging.error(str(e))
    def close(self):
        try:
            self.cursor.close()
            self.conn.close()
            logging.info("INFO, close success")
        except Exception as e:
            logging.error(str(e))

    #--------------------------------------------------------------------------------------------------------
    #从数据库读取数据
    #--------------------------------------------------------------------------------------------------------
    def get_tbl_accountinfo(self):
        try:
            sql="""SELECT accountName,appid,accountId,isActive,pwd,cid FROM accountInfo where isActive=1"""
            cnt=self.cursor.execute(sql)
            ret=self.cursor.fetchall()
            ret_list = []
            for item in ret:
                ret_list.append(item)
            return ret_list
        except Exception as e:
            logging.error(str(e))

    def save_tbl_accountinfo(self):
        try:
            sql="""SELECT accountName,appid,accountId,isActive,pwd,cid FROM accountInfo where isActive=1"""
            cnt=self.cursor.execute(sql)
            ret=self.cursor.fetchall()
            ret_list = []
            for item in ret:
                ret_list.append(item)

            index=0
            accountinfoAll = open("accountinfoAll.txt", 'w')
            while(index<len(ret_list)):
                accountinfoAll.write(str(ret_list[index][0])+" "+str(ret_list[index][1])+" "+str(index)+" "+str(ret_list[index][3]))
                accountinfoAll.write("\n")
                index=index+1
        except Exception as e:
            logging.error(str(e))

    def save_tbl_cid(self):
        try:
            sql="""SELECT accountName,cid FROM accountInfo where isActive =1 group by accountName,cid"""
            cnt=self.cursor.execute(sql)
            ret=self.cursor.fetchall()
            ret_list = []
            for item in ret:
                ret_list.append(item)

            index=0
            accountinfoAll = open("accountinfoAllCid.txt", 'w')
            while(index<len(ret_list)):
                accountinfoAll.write(str(ret_list[index][0])+" "+str(ret_list[index][1]))
                accountinfoAll.write("\n")
                index=index+1
        except Exception as e:
            logging.error(str(e))

    def add_wordclass_data(self, param):
        try:
            sql="""insert into tbl_monitortask(id,timepoint,wordclass_name,impression,click,cost) values(NULL,%s,%s,%s,%s,%s)"""
            n=self.cursor.execute(sql,param)
            last_id=int(self.cursor.lastrowid)
            self.conn.commit()
            return n,last_id
        except Exception as e:
            logging.error(str(e))
            return 0,0

if __name__ == "__main__":
    mysql = AccountInfo()
    mysql.save_tbl_accountinfo()
    mysql.close()


