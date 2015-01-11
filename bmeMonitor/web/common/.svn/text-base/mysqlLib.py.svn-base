#!/usr/bin/env python
#-*- coding: utf-8 -*-
from logLib import *
import datetime

import MySQLdb
host='10.215.73.52'
user='semrd'
passwd='semtest'
db='db_bmemonitor'
port=8111

from dynsqlLib import *

class mysqlLib():
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
    #tbl_monitormetrics查询操作
    #--------------------------------------------------------------------------------------------------------
    def query_monitormetrics(self,param):
        try:
            s=DynSql("""select id,monitorObj_id,name from tbl_monitormetrics where 1=1
            { and id=$id}
            ORDER BY id DESC {limit {$offset,} $limit}""")
            sql=s(param)
            cnt=self.cursor.execute(sql[0],sql[1])
            ret=self.cursor.fetchall()
            return ret
        except Exception as e:
            logging.error(str(e))

    #--------------------------------------------------------------------------------------------------------
    #tbl_monitortask添加新任务
    #--------------------------------------------------------------------------------------------------------
    def add_task(self, param):
        try:
            sql="""insert into tbl_monitortask(id,monitorObj_id,monitorMetrics_id,status) values(NULL,%s,%s,%s)"""
            n=self.cursor.execute(sql,param)
            last_id=int(self.cursor.lastrowid)
            self.conn.commit()
            return n,last_id
        except Exception as e:
            logging.error(str(e))
            return 0,0

    #--------------------------------------------------------------------------------------------------------
    #tbl_monitortask查询操作，查询需要启动的任务，一次查询返回一个
    #--------------------------------------------------------------------------------------------------------
    def query_monitortask_submit(self,param):
        try:
            s=DynSql("""select id,monitorObj_id,monitorMetrics_id,status from tbl_monitortask where 1=1
            { and status=$status}
            ORDER BY id ASC limit 1""")
            sql=s(param)
            cnt=self.cursor.execute(sql[0],sql[1])
            ret=self.cursor.fetchall()
            return ret
        except Exception as e:
            logging.error(str(e))

    #--------------------------------------------------------------------------------------------------------
    #tbl_monitortask更新status字段
    #--------------------------------------------------------------------------------------------------------
    def update_tbl_monitortask_status(self,param):
        try:
            sql="""update tbl_monitortask set status=%s where id=%s"""
            n=self.cursor.execute(sql,param)
            self.conn.commit()
            return n
        except Exception as e:
            logging.error(str(e))


if __name__ == "__main__":
    mysql = mysqlLib()
    mysql.close()


