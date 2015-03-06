#!/usr/bin/env python
#-*- coding: utf-8 -*-
from logLib import *
import datetime
import sys

import MySQLdb
host='10.94.54.51'
user='bmeqa'
passwd='bmeqa123'
db='db_bmemonitor'
port=8456

from dynsqlLib import *

reload(sys)
sys.setdefaultencoding( "utf-8" )

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
    #--------------------------------------------------------------------------------------------------------
    #tbl_monitortask更新starttime字段
    #--------------------------------------------------------------------------------------------------------
    def update_tbl_monitortask_starttime(self,param):
        try:
            sql="""update tbl_monitortask set startTime=%s where id=%s"""
            n=self.cursor.execute(sql,param)
            self.conn.commit()
            return n
        except Exception as e:
            logging.error(str(e))
    #--------------------------------------------------------------------------------------------------------
    #tbl_monitortask更新endtime字段
    #--------------------------------------------------------------------------------------------------------
    def update_tbl_monitortask_endtime(self,param):
        try:
            sql="""update tbl_monitortask set endTime=%s where id=%s"""
            n=self.cursor.execute(sql,param)
            self.conn.commit()
            return n
        except Exception as e:
            logging.error(str(e))
    #--------------------------------------------------------------------------------------------------------
    #tbl_monitordata添加监控数据
    #--------------------------------------------------------------------------------------------------------
    def add_tbl_monitordata(self, param):
        try:
            sql="""insert into tbl_monitordata(id,monitorTask_id,status,info) values(NULL,%s,%s,%s)"""
            n=self.cursor.execute(sql,param)
            last_id=int(self.cursor.lastrowid)
            self.conn.commit()
            return n,last_id
        except Exception as e:
            logging.error(str(e))
            return 0,0
    #--------------------------------------------------------------------------------------------------------
    #tbl_alarmconf查询操作，查询监控指标对应的告警配置信息
    #--------------------------------------------------------------------------------------------------------
    def query_tbl_alarmconf(self,param):
        try:
            s=DynSql("""select id,monitorObj_id,monitorMetrics_id,name,description,status,conf,info from tbl_alarmconf where 1=1
            { and monitorObj_id=$monitorObj_id} { and monitorMetrics_id=$monitorMetrics_id}
            ORDER BY id ASC limit 1""")
            sql=s(param)
            cnt=self.cursor.execute(sql[0],sql[1])
            ret=self.cursor.fetchall()
            return ret
        except Exception as e:
            logging.error(str(e))
    #--------------------------------------------------------------------------------------------------------
    #tbl_alarmobj添加新任务
    #--------------------------------------------------------------------------------------------------------
    def add_alarmobj(self, param):
        try:
            sql="""insert into tbl_alarmobj(id,alarmConf_id,monitorTask_id,monitorObj_id,monitorMetrics_id,description,status,datetime) values(NULL,%s,%s,%s,%s,%s,%s,%s)"""
            n=self.cursor.execute(sql,param)
            last_id=int(self.cursor.lastrowid)
            self.conn.commit()
            return n,last_id
        except Exception as e:
            logging.error(str(e))
            return 0,0
    #--------------------------------------------------------------------------------------------------------
    #tbl_alarmobj查询操作，查询历史告警列表
    #--------------------------------------------------------------------------------------------------------
    def query_tbl_alarmobj(self,param):
        try:
            s=DynSql("""select id,alarmConf_id,monitorTask_id,monitorObj_id,monitorMetrics_id,description,status,datetime,inactive_datetime,cause,handleBy,info from tbl_alarmobj where 1=1
            { and id=$id} { and alarmConf_id=$alarmConf_id} { and monitorObj_id=$monitorObj_id} { and monitorMetrics_id=$monitorMetrics_id}
            { and status=$status}
            ORDER BY id DESC {limit {$offset,} $limit}""")
            sql=s(param)
            cnt=self.cursor.execute(sql[0],sql[1])
            ret=self.cursor.fetchall()
            return ret
        except Exception as e:
            logging.error(str(e))
    #--------------------------------------------------------------------------------------------------------
    #tbl_alarmobj查询操作，查询历史告警总数
    #--------------------------------------------------------------------------------------------------------
    def query_alarm_totalcnt(self,param):
        try:
            s=DynSql("""select count(*) from tbl_alarmobj where 1=1
            """)
            sql=s(param)
            cnt=self.cursor.execute(sql[0],sql[1])
            ret=self.cursor.fetchall()
            totalcnt=ret[0][0]
            return ret
        except Exception as e:
            logging.error(str(e))
    #--------------------------------------------------------------------------------------------------------
    #tbl_alarmobj查询操作，查询一段时间历史新增告警
    #--------------------------------------------------------------------------------------------------------
    def query_alarm_dayperiod(self,dayperiod):
        try:
            sql = """select date(datetime),count(*) from tbl_alarmobj  where DATE_SUB(CURDATE(), INTERVAL """ + str(dayperiod) + """ DAY) <= date(datetime) group by date(datetime)
            """
            cnt=self.cursor.execute(sql)
            ret=self.cursor.fetchall()
            return ret
        except Exception as e:
            logging.error(str(e))
    #--------------------------------------------------------------------------------------------------------
    #tbl_alarmobj更新inactive_datetime字段
    #--------------------------------------------------------------------------------------------------------
    def update_tbl_tbl_alarmobj_inactive_datetime(self,param):
        try:
            sql="""update tbl_alarmobj set inactive_datetime=%s where id=%s"""
            n=self.cursor.execute(sql,param)
            self.conn.commit()
            return n
        except Exception as e:
            logging.error(str(e))
    #--------------------------------------------------------------------------------------------------------
    #tbl_alarmobj更新cause、handby、status字段
    #--------------------------------------------------------------------------------------------------------
    def update_tbl_tbl_alarmobj_inactive_datetime_alarminfo(self,param):
        try:
            sql="""update tbl_alarmobj set status=%s,cause=%s,handleBy=%s where id=%s"""
            #print sql
            n=self.cursor.execute(sql,param)
            self.conn.commit()
            return n
        except Exception as e:
            logging.error(str(e))
    #--------------------------------------------------------------------------------------------------------
    #tbl_wordclass_data写入操作
    #--------------------------------------------------------------------------------------------------------
    def add_wordclass_data(self, param):
        try:
            sql="""insert into tbl_wordclass_data(id,timepoint,wordclass_name,impression,click,cost) values(NULL,%s,%s,%s,%s,%s)"""
            n=self.cursor.execute(sql,param)
            last_id=int(self.cursor.lastrowid)
            self.conn.commit()
            return n,last_id
        except Exception as e:
            logging.error(str(e))
            return 0,0
    #--------------------------------------------------------------------------------------------------------
    #tbl_wordclass_data查询操作
    #--------------------------------------------------------------------------------------------------------
    def query_wordclass_data(self, param, function):
        try:
            sql="""select wordclass_name,"""+function+""" from tbl_wordclass_data where timepoint=%s"""
            cnt=self.cursor.execute(sql,param)
            ret=self.cursor.fetchall()
            return ret
        except Exception as e:
            logging.error(str(e))
            return 0,0
    #--------------------------------------------------------------------------------------------------------
    #tbl_url_data写入
    #--------------------------------------------------------------------------------------------------------
    def add_url_data(self, param):
        try:
            sql="""insert into tbl_url_data(id,monitorTask_id,timepoint,accountName,totalurlNum,errorurlNum,deadDealNum,badDeadDealNum,openurlErrorNum,noListResultNum,errorCidNum,formatErrorNum,nullUrlNum) values(NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            n=self.cursor.execute(sql,param)
            last_id=int(self.cursor.lastrowid)
            self.conn.commit()
            return n,last_id
        except Exception as e:
            logging.error(str(e))
            return 0,0
    #--------------------------------------------------------------------------------------------------------
    #tbl_url_data查询id
    #--------------------------------------------------------------------------------------------------------
    def get_url_data_id(self, param):
        try:
            sql="""select id from tbl_url_data where accountName=%s and timepoint=%s"""
            cnt=self.cursor.execute(sql,param)
            ret=self.cursor.fetchall()
            return ret[0][0]
        except Exception as e:
            logging.error(str(e))
            return 0,0
    #--------------------------------------------------------------------------------------------------------
    #tbl_url_data写入
    #--------------------------------------------------------------------------------------------------------
    def add_urlerror_data(self, param):
        try:
            sql="""insert into tbl_errorurl(id,urldataid,accountname,plan,cell,keyword,discription,url,pc_mobile,timepoint) values(NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            n=self.cursor.execute(sql,param)
            last_id=int(self.cursor.lastrowid)
            self.conn.commit()
            return n,last_id
        except Exception as e:
            logging.error(str(e))
            return 0,0
    #--------------------------------------------------------------------------------------------------------
    #tbl_url_data写入
    #--------------------------------------------------------------------------------------------------------
    def query_urlalarm_data(self,param):
        try:
            sql="""select * from tbl_url_data where timepoint=%s and errorurlNum>%s"""
            cnt=self.cursor.execute(sql,param)
            ret=self.cursor.fetchall()
            return ret
        except Exception as e:
            logging.error(str(e))
            return 0,0
    #--------------------------------------------------------------------------------------------------------
    #tbl_monitortask 监控指标-监控任务列表查询
    #--------------------------------------------------------------------------------------------------------
    def query_tbl_monitortask_list(self,param):
        try:
            sql="""select id from tbl_monitortask where monitorMetrics_id=%s and startTime>%s and startTime<%s and status=4"""
            cnt=self.cursor.execute(sql,param)
            ret=self.cursor.fetchall()
            return ret
        except Exception as e:
            logging.error(str(e))
            return 0,0
    #--------------------------------------------------------------------------------------------------------
    #tbl_monitortask 查询监控指标对应的账户余额信息
    #--------------------------------------------------------------------------------------------------------
    def query_tbl_monitordata_account_info(self,param):
        try:
            sql="""select info from tbl_monitordata where monitorTask_id=%s"""
            cnt=self.cursor.execute(sql,param)
            ret=self.cursor.fetchall()
            return ret
        except Exception as e:
            logging.error(str(e))
            return 0,0
    #--------------------------------------------------------------------------------------------------------
    #tbl_url_data 查询监控指标对应的账户余额信息
    #--------------------------------------------------------------------------------------------------------
    def query_tbl_url_data(self,param):
        try:
            sql="""select accountName from tbl_url_data where monitorTask_id=%s"""
            cnt=self.cursor.execute(sql,param)
            ret=self.cursor.fetchall()
            return ret
        except Exception as e:
            logging.error(str(e))
            return 0,0
    #--------------------------------------------------------------------------------------------------------
    #tbl_url_data 查询监控指标对应的url信息
    #--------------------------------------------------------------------------------------------------------
    def query_tbl_url_data_info(self,param):
        try:
            sql="select id,timepoint,accountName,totalurlNum,errorurlNum,deadDealNum,badDeadDealNum,openurlErrorNum,noListResultNum,errorCidNum,formatErrorNum,nullUrlNum from tbl_url_data ORDER BY %s %s limit %s, %s"
            #print sql %param
            cnt=self.cursor.execute(sql,param)
            ret=self.cursor.fetchall()
            return ret
        except Exception as e:
            logging.error(str(e))
            return 0,0
    #--------------------------------------------------------------------------------------------------------
    #tbl_errorurl 查询监控指标记录总数
    #--------------------------------------------------------------------------------------------------------
    def query_tbl_url_data_info_cnt(self):
        try:
            sql="""select count(*) from tbl_url_data"""
            cnt=self.cursor.execute(sql)
            ret=self.cursor.fetchall()
            return ret
        except Exception as e:
            logging.error(str(e))
            return 0,0
    #--------------------------------------------------------------------------------------------------------
    def query_tbl_url_data_detail_info(self,param):
        try:
            sql="select id,accountname,plan,cell,keyword,discription,url,pc_mobile,timepoint from tbl_errorurl where urldataid=%s ORDER BY %s %s limit %s, %s"
            #print sql %param
            cnt=self.cursor.execute(sql,param)
            ret=self.cursor.fetchall()
            return ret
        except Exception as e:
            logging.error(str(e))
            return 0,0
    #--------------------------------------------------------------------------------------------------------
    #tbl_errorurl 查询监控指标记录总数
    #--------------------------------------------------------------------------------------------------------
    def query_tbl_url_data_detail_info_cnt(self,param):
        try:
            sql="select count(*) from tbl_errorurl where urldataid=%s"
            cnt=self.cursor.execute(sql,param)
            ret=self.cursor.fetchall()
            return ret
        except Exception as e:
            logging.error(str(e))
            return 0,0
    #--------------------------------------------------------------------------------------------------------
    #tbl_wordclass_data 查询word列表
    #--------------------------------------------------------------------------------------------------------
    def query_tbl_wordclass_data(self,param):
        try:
            sql="select distinct(wordclass_name) from tbl_wordclass_data"
            cnt=self.cursor.execute(sql,param)
            ret=self.cursor.fetchall()
            return ret
        except Exception as e:
            logging.error(str(e))
            return 0,0
    #--------------------------------------------------------------------------------------------------------
    #tbl_wordclass_data 查询word信息
    #--------------------------------------------------------------------------------------------------------
    def query_tbl_wordclass_data_info(self,param):
        try:
            sql="select timepoint,impression,click,cost from tbl_wordclass_data where wordclass_name=%s and timepoint>=%s and timepoint<=%s order by timepoint desc"
            cnt=self.cursor.execute(sql,param)
            ret=self.cursor.fetchall()
            return ret
        except Exception as e:
            logging.error(str(e))
            return 0,0
    #--------------------------------------------------------------------------------------------------------
    #tbl_alarmobj查询操作，查询监控指标相关历史告警列表
    #--------------------------------------------------------------------------------------------------------
    def query_tbl_alarmobj_metrics_related(self,param):
        try:
            sql = """select id,description,status,datetime,inactive_datetime,cause,handleBy,info from tbl_alarmobj where monitorMetrics_id=%s
            ORDER BY %s %s limit %s,%s"""
            cnt=self.cursor.execute(sql,param)
            ret=self.cursor.fetchall()
            return ret
        except Exception as e:
            logging.error(str(e))
    #--------------------------------------------------------------------------------------------------------
    #tbl_alarmobj查询操作，查询监控指标相关历史告警总数
    #--------------------------------------------------------------------------------------------------------
    def query_tbl_alarmobj_metrics_related_cnt(self,param):
        try:
            sql = """select count(*) from tbl_alarmobj where monitorMetrics_id=%s"""
            cnt=self.cursor.execute(sql,param)
            ret=self.cursor.fetchall()
            return ret
        except Exception as e:
            logging.error(str(e))
    #--------------------------------------------------------------------------------------------------------
    #queryClickURLData查询操作，查询链接跳转监控数据总数
    #--------------------------------------------------------------------------------------------------------
    def query_queryClickURLData_cnt(self):
        try:
            sql = "SELECT count(*) FROM tbl_monitordata WHERE info like '%expLoc%'"
            cnt=self.cursor.execute(sql)
            ret=self.cursor.fetchall()
            return ret
        except Exception as e:
            logging.error(str(e))
    #--------------------------------------------------------------------------------------------------------
    #queryClickURLData查询操作，查询链接跳转监控数据
    #--------------------------------------------------------------------------------------------------------
    def query_queryClickURLData_info(self,param):
        try:
            sql = "SELECT id,info FROM tbl_monitordata WHERE info like '%expLoc%' ORDER BY " + param[0] + " " + param[1] + " limit " + str(param[2]) + "," + str(param[3])
            cnt=self.cursor.execute(sql)
            ret=self.cursor.fetchall()
            return ret
        except Exception as e:
            logging.error(str(e))
    #--------------------------------------------------------------------------------------------------------
    #queryCookieInfoData查询操作，查询cookie埋点监控数据总数
    #--------------------------------------------------------------------------------------------------------
    def query_queryCookieInfoData_cnt(self):
        try:
            sql = "SELECT count(*) FROM tbl_monitordata WHERE info like '%expCpsId%'"
            cnt=self.cursor.execute(sql)
            ret=self.cursor.fetchall()
            return ret
        except Exception as e:
            logging.error(str(e))
    #--------------------------------------------------------------------------------------------------------
    #queryCookieInfoData查询操作，查询cookie埋监控数据
    #--------------------------------------------------------------------------------------------------------
    def query_queryCookieInfoData_info(self,param):
        try:
            sql = "SELECT id,info FROM tbl_monitordata WHERE info like '%expCpsId%' ORDER BY " + param[0] + " " + param[1] + " limit " + str(param[2]) + "," + str(param[3])
            cnt=self.cursor.execute(sql)
            ret=self.cursor.fetchall()
            return ret
        except Exception as e:
            logging.error(str(e))
    #--------------------------------------------------------------------------------------------------------
    #queryVerifyInfoData查询操作，查询cookie埋点监控数据总数
    #--------------------------------------------------------------------------------------------------------
    def query_queryVerifyInfoData_cnt(self):
        try:
            sql = "SELECT count(*) FROM tbl_monitordata WHERE info like '%ftp%'"
            cnt=self.cursor.execute(sql)
            ret=self.cursor.fetchall()
            return ret
        except Exception as e:
            logging.error(str(e))
    #--------------------------------------------------------------------------------------------------------
    #queryCookieInfoData查询操作，查询cookie埋监控数据
    #--------------------------------------------------------------------------------------------------------
    def query_queryVerifyInfoData_info(self,param):
        try:
            sql = "SELECT id,info FROM tbl_monitordata WHERE info like '%ftp%' ORDER BY " + param[0] + " " + param[1] + " limit " + str(param[2]) + "," + str(param[3])
            cnt=self.cursor.execute(sql)
            ret=self.cursor.fetchall()
            return ret
        except Exception as e:
            logging.error(str(e))
    #--------------------------------------------------------------------------------------------------------
    #queryPushSuccessInfoData查询操作，查询push success监控数据总数
    #--------------------------------------------------------------------------------------------------------
    def query_queryPushSuccessInfoData_cnt(self):
        try:
            sql = "SELECT count(*) FROM tbl_monitordata WHERE info like '%totalSuccess%'"
            cnt=self.cursor.execute(sql)
            ret=self.cursor.fetchall()
            return ret
        except Exception as e:
            logging.error(str(e))
    #--------------------------------------------------------------------------------------------------------
    #queryPushSuccessInfoData查询操作，查询push success监控数据
    #--------------------------------------------------------------------------------------------------------
    def query_queryPushSuccessInfoData_info(self,param):
        try:
            sql = "SELECT id,info FROM tbl_monitordata WHERE info like '%totalSuccess%' ORDER BY " + param[0] + " " + param[1] + " limit " + str(param[2]) + "," + str(param[3])
            cnt=self.cursor.execute(sql)
            ret=self.cursor.fetchall()
            return ret
        except Exception as e:
            logging.error(str(e))
    #--------------------------------------------------------------------------------------------------------
    #queryPushFailInfoData查询操作，查询push fail监控数据总数
    #--------------------------------------------------------------------------------------------------------
    def query_queryPushFailInfoData_cnt(self):
        try:
            sql = "SELECT count(*) FROM tbl_monitordata WHERE info like '%totalFail%'"
            cnt=self.cursor.execute(sql)
            ret=self.cursor.fetchall()
            return ret
        except Exception as e:
            logging.error(str(e))
    #--------------------------------------------------------------------------------------------------------
    #queryPushFailInfoData查询操作，查询push fail监控数据
    #--------------------------------------------------------------------------------------------------------
    def query_queryPushFailInfoData_info(self,param):
        try:
            sql = "SELECT id,info FROM tbl_monitordata WHERE info like '%totalFail%' ORDER BY " + param[0] + " " + param[1] + " limit " + str(param[2]) + "," + str(param[3])
            cnt=self.cursor.execute(sql)
            ret=self.cursor.fetchall()
            return ret
        except Exception as e:
            logging.error(str(e))
    #--------------------------------------------------------------------------------------------------------
    #tbl_zhixin_monitordata写入
    #--------------------------------------------------------------------------------------------------------
    def add_zhixin_monitordata(self, param):
        try:
            sql="""insert into tbl_zhixin_monitordata(id,monitortask_id,hostname,date,city_id,srcID,flow,as_null,as_delay,zhixin_null,zhixin_delay,flag) values(NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            n=self.cursor.execute(sql,param)
            last_id=int(self.cursor.lastrowid)
            self.conn.commit()
            return n,last_id
        except Exception as e:
            logging.error(str(e))
            return 0,0
    #--------------------------------------------------------------------------------------------------------
    #query_tbl_zhixin_monitordata_hostlist查询操作，查询主机列表
    #--------------------------------------------------------------------------------------------------------
    def query_tbl_zhixin_monitordata_hostlist(self,param):
        try:
            sql = "select distinct(hostname) from tbl_zhixin_monitordata where flag=%s"
            cnt=self.cursor.execute(sql,param)
            ret=self.cursor.fetchall()
            return ret
        except Exception as e:
            logging.error(str(e))
    #--------------------------------------------------------------------------------------------------------
    #query_tbl_zhixin_monitordata查询操作，查询zhixin延迟监控数据
    #--------------------------------------------------------------------------------------------------------
    def query_tbl_zhixin_monitordata_delay(self,param):
        try:
            sql = "select date,as_delay,zhixin_delay from tbl_zhixin_monitordata where date >= %s and date <= %s and hostname = %s and city_id = %s and srcID = %s and flag=%s"
            cnt=self.cursor.execute(sql,param)
            ret=self.cursor.fetchall()
            return ret
        except Exception as e:
            logging.error(str(e))
    #--------------------------------------------------------------------------------------------------------
    #query_tbl_zhixin_monitordata查询操作，查询zhixin流量监控数据
    #--------------------------------------------------------------------------------------------------------
    def query_tbl_zhixin_monitordata_flow(self,param):
        try:
            sql = "select date,flow from tbl_zhixin_monitordata where date >= %s and date <= %s and hostname = %s and city_id = %s and srcID = %s and flag=%s"
            cnt=self.cursor.execute(sql,param)
            ret=self.cursor.fetchall()
            return ret
        except Exception as e:
            logging.error(str(e))
    #--------------------------------------------------------------------------------------------------------
    #query_tbl_zhixin_monitordata查询操作，查询zhixin流量监控数据
    #--------------------------------------------------------------------------------------------------------
    def query_tbl_zhixin_monitordata_null(self,param):
        try:
            sql = "select date,as_null,zhixin_null from tbl_zhixin_monitordata where date >= %s and date <= %s and hostname = %s and city_id = %s and srcID = %s and flag=%s"
            cnt=self.cursor.execute(sql,param)
            ret=self.cursor.fetchall()
            return ret
        except Exception as e:
            logging.error(str(e))
    #--------------------------------------------------------------------------------------------------------
    #查询账户余额-账户列表
    #--------------------------------------------------------------------------------------------------------
    def query_account_name_list(self,param):
        try:
            sql = "select info from tbl_monitordata where info like '%balance%' limit 1"
            cnt=self.cursor.execute(sql)
            ret=self.cursor.fetchall()
            return ret
        except Exception as e:
            logging.error(str(e))
    #--------------------------------------------------------------------------------------------------------
    #查询点击量-账户列表
    #--------------------------------------------------------------------------------------------------------
    def query_account_click_list(self,param):
        try:
            sql = "select info from tbl_monitordata where info like '%clickrate%' limit 1"
            cnt=self.cursor.execute(sql)
            ret=self.cursor.fetchall()
            return ret
        except Exception as e:
            logging.error(str(e))
    #--------------------------------------------------------------------------------------------------------
    #更新SEO监控数据表
    #--------------------------------------------------------------------------------------------------------
    def update_tbl_seo(self,param):
        try:
            sql="""update tbl_seo set total=%s,normal=%s,exception=%s,detailinfo=%s,uptime=%s where type=%s"""
            #print sql
            n=self.cursor.execute(sql,param)
            self.conn.commit()
            return n
        except Exception as e:
            logging.error(str(e))
    #--------------------------------------------------------------------------------------------------------
    #查询SEO
    #--------------------------------------------------------------------------------------------------------
    def query_tbl_seo(self,param):
        try:
            sql = "select total,normal,exception,detailinfo from tbl_seo where type=%s"
            cnt=self.cursor.execute(sql,param)
            ret=self.cursor.fetchall()
            return ret
        except Exception as e:
            logging.error(str(e))


if __name__ == "__main__":
    mysql = mysqlLib()
    mysql.close()


