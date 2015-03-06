#!/usr/bin/env python
#-*- coding: utf-8 -*-
import tornado.web
import tornado.httpserver
import tornado.options
import tornado.ioloop
from tornado.options import define,options

import sys
import os
import time
import json
import traceback

from com.logLib import *
from com.mysqlLib import *
from com.cmdLib import *
from com.confLib import *
from com.jsonLib import *

import urlparse

defaultport=8868
import socket
hostname=socket.gethostname()
hostname=socket.gethostbyname(hostname)
#print hostname

import re
import urllib
#CAS setting
CAS_SETTINGS = {
	#replace this with your cas server url
	#'cas_server' : 'https://uuap.baidu.com/',
    'cas_server' : 'http://itebeta.baidu.com:8100',

	#replace this with your website url
	'service_url' : "http://"+hostname+":"+str(defaultport)+"/",
	#CAS protocol version, 1.0 or 2.0? default is 2.0.
	'version' : 2
}

log_init("./log/bmeMonitor.log")

########################################
class authenticateBase(tornado.web.RequestHandler):
    def get_upps_user(self):
        #what you finally get
        userid = None
        try:
            server_ticket = self.get_argument( 'ticket' )
        except Exception, e:
            #print(str(e))
            return userid
        #validate the STprint server_ticket
        validate_suffix = '/validate' if CAS_SETTINGS[ 'version' ] == 1 else '/proxyValidate'
        validate_url = CAS_SETTINGS[ 'cas_server'] + validate_suffix + '?service=' + urllib.quote( CAS_SETTINGS[ 'service_url' ] ) + '&ticket=' + urllib.quote( server_ticket )
        #validate_url = CAS_SETTINGS[ 'cas_server'] + validate_suffix + '?service=' + urllib.quote( CAS_SETTINGS[ 'service_url' ] )
        response = urllib.urlopen( validate_url ).read()
        pattern = r'<cas:user>(.*)</cas:user>'
        match = re.search( pattern, response )
        if match:
            userid = match.groups()[ 0 ]
        if not userid:
            pass
        return userid
    def get_cookie_user(self):
        return self.get_secure_cookie("user")

class LoginHandler(authenticateBase):
    def get(self):
        userid=self.get_upps_user()
        if(userid):
            self.set_secure_cookie("user",userid)
            self.render("demo/monitor.html",usrname=userid)
        else:
            redirect_url = CAS_SETTINGS[ 'cas_server' ] + '/login?service=' + CAS_SETTINGS[ 'service_url' ]
            self.redirect( redirect_url )

class LogoutHandler(tornado.web.RequestHandler):
    def get( self ):
        #redirect to cas server
        self.clear_cookie("user")
        redirect_url = CAS_SETTINGS[ 'cas_server' ] + '/logout'
        self.redirect( redirect_url )
########################################
class nav(authenticateBase):
    def get(self):
        userid=self.get_cookie_user()
        if(userid):
            self.render("./demo/nav.html", usrname=userid)
        else:
            redirect_url=CAS_SETTINGS[ 'cas_server' ] + '/login?service=' + CAS_SETTINGS[ 'service_url' ]
            self.redirect(redirect_url)
class monitor(authenticateBase):
    def get(self):
        userid=self.get_cookie_user()
        if(userid):
            self.render("./demo/monitor.html", usrname=userid)
        else:
            redirect_url=CAS_SETTINGS[ 'cas_server' ] + '/login?service=' + CAS_SETTINGS[ 'service_url' ]
            self.redirect(redirect_url)
class helpcls(authenticateBase):
    def get(self):
        userid=self.get_cookie_user()
        if(userid):
            self.render("./demo/help.html", usrname=userid)
        else:
            redirect_url=CAS_SETTINGS[ 'cas_server' ] + '/login?service=' + CAS_SETTINGS[ 'service_url' ]
            self.redirect(redirect_url)
class querytreedata(authenticateBase):
    def post(self):
        monitor_tree_data = parse_conf("./conf/monitor.conf")
        mysql = mysqlLib()
        param = {}
        alarmlist = mysql.query_tbl_alarmobj(param)
        #print alarmlist
        alarm_stat_all = {}
        alarm_stat_inactive = {}
        alarm_stat_active = {}
        for item in alarmlist:
            if(int(item[6]) == 0):
                alarmo_monitorMetrics_id = int(item[4])
                if(alarmo_monitorMetrics_id not in alarm_stat_active):
                    alarm_stat_active[alarmo_monitorMetrics_id] = 1
                else:
                    alarm_stat_active[alarmo_monitorMetrics_id] += 1
                if(alarmo_monitorMetrics_id not in alarm_stat_all):
                    alarm_stat_all[alarmo_monitorMetrics_id] = 1
                else:
                    alarm_stat_all[alarmo_monitorMetrics_id] += 1
            elif(int(item[6]) == 1):
                alarmo_monitorMetrics_id = int(item[4])
                if(alarmo_monitorMetrics_id not in alarm_stat_inactive):
                    alarm_stat_inactive[alarmo_monitorMetrics_id] = 1
                else:
                    alarm_stat_inactive[alarmo_monitorMetrics_id] += 1
                if(alarmo_monitorMetrics_id not in alarm_stat_all):
                    alarm_stat_all[alarmo_monitorMetrics_id] = 1
                else:
                    alarm_stat_all[alarmo_monitorMetrics_id] += 1

        #i,j,k = searchNode(monitor_tree_data, 1)
        #print i,j,k
        for item in alarm_stat_active:
            i,j,k = searchNode(monitor_tree_data, int(item))
            #BME告警统计
            if(monitor_tree_data[0]['tags'] == []):
                monitor_tree_data[0]['tags'].append(str(alarm_stat_active[item]))
            else:
                tmp = int(monitor_tree_data[0]['tags'][0])
                monitor_tree_data[0]['tags'][0] = str(tmp + alarm_stat_active[item])
            #二级菜单如SEM告警统计
            if(monitor_tree_data[0]['nodes'][i]['tags'] == []):
                monitor_tree_data[0]['nodes'][i]['tags'].append(str(alarm_stat_active[item]))
            else:
                tmp = int(monitor_tree_data[0]['nodes'][i]['tags'][0])
                monitor_tree_data[0]['nodes'][i]['tags'][0] = str(tmp + alarm_stat_active[item])
            #三级菜单如账户监控告警统计
            if(monitor_tree_data[0]['nodes'][i]['nodes'][j]['tags'] == []):
                monitor_tree_data[0]['nodes'][i]['nodes'][j]['tags'].append(str(alarm_stat_active[item]))
            else:
                tmp = int(monitor_tree_data[0]['nodes'][i]['nodes'][j]['tags'][0])
                monitor_tree_data[0]['nodes'][i]['nodes'][j]['tags'][0] = str(tmp + alarm_stat_active[item])
            #四级菜单如账户余额告警统计
            if(monitor_tree_data[0]['nodes'][i]['nodes'][j]['nodes'][k]['tags'] == []):
                monitor_tree_data[0]['nodes'][i]['nodes'][j]['nodes'][k]['tags'].append(str(alarm_stat_active[item]))
            else:
                tmp = int(monitor_tree_data[0]['nodes'][i]['nodes'][j]['nodes'][k]['tags'][0])
                monitor_tree_data[0]['nodes'][i]['nodes'][j]['nodes'][k]['tags'][0] = str(tmp + alarm_stat_active[item])
        for item in alarm_stat_all:
            i,j,k = searchNode(monitor_tree_data, int(item))
            #BME告警统计
            if(monitor_tree_data[0]['alarm_all'] == []):
                monitor_tree_data[0]['alarm_all'].append(str(alarm_stat_all[item]))
            else:
                tmp = int(monitor_tree_data[0]['alarm_all'][0])
                monitor_tree_data[0]['alarm_all'][0] = str(tmp + alarm_stat_all[item])
            #二级菜单如SEM告警统计
            if(monitor_tree_data[0]['nodes'][i]['alarm_all'] == []):
                monitor_tree_data[0]['nodes'][i]['alarm_all'].append(str(alarm_stat_all[item]))
            else:
                tmp = int(monitor_tree_data[0]['nodes'][i]['alarm_all'][0])
                monitor_tree_data[0]['nodes'][i]['alarm_all'][0] = str(tmp + alarm_stat_all[item])
            #三级菜单如账户监控告警统计
            if(monitor_tree_data[0]['nodes'][i]['nodes'][j]['alarm_all'] == []):
                monitor_tree_data[0]['nodes'][i]['nodes'][j]['alarm_all'].append(str(alarm_stat_all[item]))
            else:
                tmp = int(monitor_tree_data[0]['nodes'][i]['nodes'][j]['alarm_all'][0])
                monitor_tree_data[0]['nodes'][i]['nodes'][j]['alarm_all'][0] = str(tmp + alarm_stat_all[item])
            #四级菜单如账户余额告警统计
            if(monitor_tree_data[0]['nodes'][i]['nodes'][j]['nodes'][k]['alarm_all'] == []):
                monitor_tree_data[0]['nodes'][i]['nodes'][j]['nodes'][k]['alarm_all'].append(str(alarm_stat_all[item]))
            else:
                tmp = int(monitor_tree_data[0]['nodes'][i]['nodes'][j]['nodes'][k]['alarm_all'][0])
                monitor_tree_data[0]['nodes'][i]['nodes'][j]['nodes'][k]['alarm_all'][0] = str(tmp + alarm_stat_all[item])
        for item in alarm_stat_inactive:
            i,j,k = searchNode(monitor_tree_data, int(item))
            #BME告警统计
            if(monitor_tree_data[0]['alarm_inactive'] == []):
                monitor_tree_data[0]['alarm_inactive'].append(str(alarm_stat_inactive[item]))
            else:
                tmp = int(monitor_tree_data[0]['alarm_inactive'][0])
                monitor_tree_data[0]['alarm_inactive'][0] = str(tmp + alarm_stat_inactive[item])
            #二级菜单如SEM告警统计
            if(monitor_tree_data[0]['nodes'][i]['alarm_inactive'] == []):
                monitor_tree_data[0]['nodes'][i]['alarm_inactive'].append(str(alarm_stat_inactive[item]))
            else:
                tmp = int(monitor_tree_data[0]['nodes'][i]['alarm_inactive'][0])
                monitor_tree_data[0]['nodes'][i]['alarm_inactive'][0] = str(tmp + alarm_stat_inactive[item])
            #三级菜单如账户监控告警统计
            if(monitor_tree_data[0]['nodes'][i]['nodes'][j]['alarm_inactive'] == []):
                monitor_tree_data[0]['nodes'][i]['nodes'][j]['alarm_inactive'].append(str(alarm_stat_inactive[item]))
            else:
                tmp = int(monitor_tree_data[0]['nodes'][i]['nodes'][j]['alarm_inactive'][0])
                monitor_tree_data[0]['nodes'][i]['nodes'][j]['alarm_inactive'][0] = str(tmp + alarm_stat_inactive[item])
            #四级菜单如账户余额告警统计
            if(monitor_tree_data[0]['nodes'][i]['nodes'][j]['nodes'][k]['alarm_inactive'] == []):
                monitor_tree_data[0]['nodes'][i]['nodes'][j]['nodes'][k]['alarm_inactive'].append(str(alarm_stat_inactive[item]))
            else:
                tmp = int(monitor_tree_data[0]['nodes'][i]['nodes'][j]['nodes'][k]['alarm_inactive'][0])
                monitor_tree_data[0]['nodes'][i]['nodes'][j]['nodes'][k]['alarm_inactive'][0] = str(tmp + alarm_stat_inactive[item])
        #print monitor_tree_data
        self.write(json.dumps(monitor_tree_data))

class queryMonitorMetricsData(authenticateBase):
    def post(self):
        monitor_tree_data = parse_conf("./conf/monitor.conf")
        MonitorMetricsData = queryMonitorMetrics(monitor_tree_data)
        #print MonitorMetricsData
        self.write(json.dumps(MonitorMetricsData))
class queryAlarmDayperiod(authenticateBase):
    def post(self):
        dayperiod = 7
        mysql = mysqlLib()
        ret = mysql.query_alarm_dayperiod(dayperiod)
        mysql.close()
        #print ret
        tmp_alarm_trend = {}
        for item in ret:
            tmp_alarm_trend[str(item[0])] = item[1]
        #cutime=datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")
        cutime = datetime.datetime.now().strftime("%Y-%m-%d")
        cutime = datetime.datetime.strptime(cutime,"%Y-%m-%d")
        startdate = cutime - datetime.timedelta(days=dayperiod)
        tmp_alarm_trend_date = []
        for i in xrange(dayperiod + 1):
            day=startdate+datetime.timedelta(days=i)
            day=day.strftime('%Y-%m-%d')
            #print day
            tmp_alarm_trend_date.append(day)
            if(day not in tmp_alarm_trend):
                tmp_alarm_trend[day] = 0

        tmp_alarm_trend_cnt = []
        for item in tmp_alarm_trend_date:
            tmp_alarm_trend_cnt.append(tmp_alarm_trend[item])
        alarm_trend = {"date":tmp_alarm_trend_date,"data":tmp_alarm_trend_cnt}
        self.write(json.dumps(alarm_trend))
class queryHistoryAlarm(authenticateBase):
    def get(self):
        try:
            userid=self.get_cookie_user()
            param={}
            mysql=mysqlLib()
            alarm_list=mysql.query_tbl_alarmobj(param)
            mysql.close()

            ret_dict=[]
            for index,item in enumerate(alarm_list):
                sub_ret_dict=[]
                '''#id
                sub_ret_dict.append(str(int(item[0])))
                #alarmConf_id
                sub_ret_dict.append(str(int(item[1])))
                #monitorTask_id
                sub_ret_dict.append(str(int(item[2])))
                #monitorObj_id
                sub_ret_dict.append(str(int(item[3])))
                #monitorMetrics_id
                sub_ret_dict.append(str(int(item[4])))
                #description
                sub_ret_dict.append(item[5])
                #status
                sub_ret_dict.append(str(int(item[6])))
                #datetime
                sub_ret_dict.append(str(item[7]))
                #inactive_datetime
                sub_ret_dict.append(str(item[8]))
                #cause
                sub_ret_dict.append(item[9])
                #handleBy
                sub_ret_dict.append(item[10])
                #info
                sub_ret_dict.append(item[11])'''
                #id
                sub_ret_dict.append(str(int(item[0])))
                monitor_tree_data = parse_conf("./conf/monitor.conf")
                i,j,k = searchNode(monitor_tree_data, int(item[4]))
                metrics_name = monitor_tree_data[0]['nodes'][i]['nodes'][j]['nodes'][k]['text']
                obj_name = monitor_tree_data[0]['nodes'][i]['nodes'][j]['text']
                #monitorObj_id
                #sub_ret_dict.append(str(int(item[3])))
                sub_ret_dict.append(obj_name)
                #monitorMetrics_id
                #sub_ret_dict.append(str(int(item[4])))
                sub_ret_dict.append(metrics_name)
                #datetime
                sub_ret_dict.append(str(item[7]))
                #status
                if(str(int(item[6])) == "0"):
                    sub_ret_dict.append(u"活动态")
                if(str(int(item[6])) == "1"):
                    sub_ret_dict.append(u"已恢复")
                #inactive_datetime
                if(str(item[8]) == 'None'):
                    sub_ret_dict.append("--")
                else:
                    sub_ret_dict.append(str(item[8]))
                #handleBy
                if(item[10] is None):
                    sub_ret_dict.append("--")
                else:
                    sub_ret_dict.append(item[10])
                cause = ""
                #cause
                if(item[9] is None):
                    sub_ret_dict.append("--")
                else:
                    sub_ret_dict.append(item[9])
                    cause = item[9]
                sub_ret_dict.append("<a href='javascript:alarmDetail(\"" + str(int(item[0])) + "\")'>详情</a> " +
                "<a href='javascript:initalarmUpdate(\"" + str(int(item[0])) + "\",\"" + str(int(item[6])) + "\",\"" + cause + "\",\"" + userid + "\")'>编辑</a>")
                ret_dict.append(sub_ret_dict)
                '''tmp_row = "row_" + str(index + 1)
                sub_ret_dict={}
                sub_ret_dict['DT_RowId'] = tmp_row
                sub_ret_dict['alarm_id'] = str(int(item[0]))
                sub_ret_dict['alarmConf_id'] = str(int(item[1]))
                sub_ret_dict['monitorTask_id'] = str(int(item[2]))
                sub_ret_dict['monitorObj_id'] = str(int(item[3]))
                sub_ret_dict['monitorMetrics_id'] = str(int(item[4]))
                sub_ret_dict['description'] = item[5]
                sub_ret_dict['status'] = str(int(item[6]))
                sub_ret_dict['datetime'] = str(item[7])
                sub_ret_dict['inactive_datetime'] = str(item[8])
                sub_ret_dict['cause'] = item[9]
                sub_ret_dict['handleBy'] = item[10]
                sub_ret_dict['info'] = item[11]
                ret_dict.append(sub_ret_dict)'''
            ret_info = {"data":ret_dict}
            #print ret_info
            self.write(json.dumps(ret_info))
        except Exception as e:
            logging.error(str(e))
            logging.info(traceback.print_exc())
class queryAlarmDetail(authenticateBase):
    def get(self):
        alarm_id = self.get_argument("alarm_id").encode('utf-8')
        mysql = mysqlLib()
        param = {"id":alarm_id}
        ret = mysql.query_tbl_alarmobj(param)
        mysql.close()
        alarm_info = {"data": ret[0][5]}
        self.write(json.dumps(alarm_info))
class updateAlarmInfo(authenticateBase):
    def post(self):
        post_param=urlparse.parse_qs(self.request.body,True)
        alarmID=post_param['alarmID'][0]
        status_cu=post_param['status_cu'][0]
        status=post_param['status'][0]
        cause=post_param['cause'][0]
        handby=post_param['handby'][0]
        '''print alarmID
        print status_cu
        print status
        print cause
        print handby'''
        param=(status,cause,handby,alarmID)
        mysql=mysqlLib()
        mysql.update_tbl_tbl_alarmobj_inactive_datetime_alarminfo(param)
        if(status_cu == "0" and status == "1"):
            cutime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            param = (cutime, alarmID)
            mysql.update_tbl_tbl_alarmobj_inactive_datetime(param)
        mysql.close()
        retcode = 0

        '''param={"limit":limit,"offset":offset}
        mysql=mysqlLib()
        tasklist=mysql.query_task(param)

        param={}
        task_totalcnt=mysql.query_task_totalcnt(param)
        mysql.close()'''

        '''serverlist_info={}
        ret_dict=[]
        for index,item in enumerate(tasklist):
            sub_ret_dict={}
            sub_ret_dict['id']=str(int(item[0]))
            sub_ret_dict['submit']=item[1]
            sub_ret_dict['jenkinsurl']=item[2]
            sub_ret_dict['jobname']=item[3]
            sub_ret_dict['build_params']=item[4]
            sub_ret_dict['status']=item[5]
            sub_ret_dict['build_number']=item[6]
            ret_dict.append(sub_ret_dict)
        serverlist_info['ret_dict']=ret_dict'''
        serverlist_info = {"retcode":retcode}
        self.write(json.dumps(serverlist_info))
class queryMetricsDataChart(authenticateBase):
    def get(self):
        userid=self.get_cookie_user()
        metricsID = self.get_argument("metricsID").encode('utf-8')
        if(userid):
            self.render("./plugins/" + metricsID + ".html", usrname=userid)
        else:
            redirect_url=CAS_SETTINGS[ 'cas_server' ] + '/login?service=' + CAS_SETTINGS[ 'service_url' ]
            self.redirect(redirect_url)

class queryAccountList(authenticateBase):
    def post(self):
        mysql = mysqlLib()
        param = ()
        ret = mysql.query_account_name_list(param)
        mysql.close()
        account_list = []
        json_arr = json.loads(ret[0][0])
        for item in json_arr:
            account_list.append(item['accountName'])
        self.write(json.dumps(account_list))

class queryAccountList_Click(authenticateBase):
    def post(self):
        mysql = mysqlLib()
        param = ()
        ret = mysql.query_account_click_list(param)
        mysql.close()
        account_list = []
        json_arr = json.loads(ret[0][0])
        for item in json_arr:
            account_list.append(item['accountName'])
        self.write(json.dumps(account_list))

class queryAccountBalance(authenticateBase):
    def post(self):
        post_param=urlparse.parse_qs(self.request.body,True)
        monitorMetrics_id = post_param['metricsID'][0]
        startdate = post_param['startdate'][0]
        enddate = post_param['enddate'][0]
        account = post_param['account'][0]
        #print monitorMetrics_id
        param=(monitorMetrics_id, startdate, enddate)
        mysql=mysqlLib()
        ret = mysql.query_tbl_monitortask_list(param)
        serverlist_info = []
        for item in ret:
            serverlist_info.append(item[0])
        cat = []
        data = []
        for item in serverlist_info:
            param = (item)
            ret = mysql.query_tbl_monitordata_account_info(param)
            ret = json.loads(ret[0][0])
            for item_item in ret:
                if(item_item['accountName'] == account):
                    cat.append(item_item['datetime'])
                    data.append(item_item['balance'])
        mysql.close()
        '''mysql = mysqlLib()
        param = ()
        ret = mysql.query_account_name_list(param)
        account_list = []
        json_arr = json.loads(ret[0][0])
        for item in json_arr:
            account_list.append(item['accountName'])'''
        account_info_list = {'cat':cat,'data':data}
        self.write(json.dumps(account_info_list))

class queryAccountClick(authenticateBase):
    def post(self):
        post_param=urlparse.parse_qs(self.request.body,True)
        monitorMetrics_id = post_param['metricsID'][0]
        startdate = post_param['startdate'][0]
        enddate = post_param['enddate'][0]
        account = post_param['account'][0]
        #print monitorMetrics_id
        param=(monitorMetrics_id, startdate, enddate)
        mysql=mysqlLib()
        ret = mysql.query_tbl_monitortask_list(param)
        serverlist_info = []
        for item in ret:
            serverlist_info.append(item[0])
        cat = []
        data0 = []
        data1 = []
        data2 = []
        data3 = []
        for item in serverlist_info:
            param = (item)
            ret = mysql.query_tbl_monitordata_account_info(param)
            ret = json.loads(ret[0][0])
            for item_item in ret:
                if(item_item['accountName'] == account):
                    cat.append(item_item['datetime'])
                    data0.append(int(item_item['clickrate'][0]))
                    data1.append(int(item_item['clickrate'][1]))
                    data2.append(int(item_item['clickrate'][2]))
                    data3.append(int(item_item['clickrate'][3]))
        mysql.close()
        '''mysql = mysqlLib()
        param = ()
        ret = mysql.query_account_name_list(param)
        account_list = []
        json_arr = json.loads(ret[0][0])
        for item in json_arr:
            account_list.append(item['accountName'])'''
        account_info_list = {'cat':cat,'data0':data0,'data1':data1,'data2':data2,'data3':data3}
        self.write(json.dumps(account_info_list))

class queryAccounts(authenticateBase):
    def post(self):
        post_param=urlparse.parse_qs(self.request.body,True)
        monitorMetrics_id=post_param['metricsID'][0]
        #print monitorMetrics_id
        param=(monitorMetrics_id)
        mysql=mysqlLib()
        ret = mysql.query_tbl_monitortask_list(param)
        tasklist_info = []
        for item in ret:
            tasklist_info.append(item[0])
        task_id = tasklist_info[-1]
        account_list = []
        param = (task_id)
        ret = mysql.query_tbl_url_data(param)
        for item in ret:
            account_list.append(item[0])
        mysql.close()
        self.write(json.dumps(account_list))


class queryTableData(authenticateBase):
    def get(self):
        userid=self.get_cookie_user()
        #page = self.get_argument("page").encode('utf-8')
        '''limit = self.get_argument("limit").encode('utf-8')
        offset = self.get_argument("offset").encode('utf-8')
        sort = self.get_argument("sort").encode('utf-8')
        order = self.get_argument("order").encode('utf-8')
        print limit,offset,sort,order'''
        if(userid):
            data = {
            "total":100,
            "rows":[
        			{
        				"name": "bootstrap-table",
        				"stargazers_count": "526",
        				"forks_count": "122",
        				"description": "An extended Bootstrap table with radio, checkbox, sort, pagination, and other added features. (supports twitter bootstrap v2 and v3) "
        			},
        			{
        				"name": "multiple-select",
        				"stargazers_count": "288",
        				"forks_count": "150",
        				"description": "A jQuery plugin to select multiple elements with checkboxes :)"
        			},
        			{
        				"name": "bootstrap-show-password",
        				"stargazers_count": "32",
        				"forks_count": "11",
        				"description": "Show/hide password plugin for twitter bootstrap."
        			},
        			{
        				"name": "blog",
        				"stargazers_count": "13",
        				"forks_count": "4",
        				"description": "my blog"
        			},
        			{
        				"name": "scutech-redmine",
        				"stargazers_count": "6",
        				"forks_count": "3",
        				"description": "Redmine notification tools for chrome extension."
        			}
        		]
            }
            self.write(json.dumps(data))
        else:
            redirect_url=CAS_SETTINGS[ 'cas_server' ] + '/login?service=' + CAS_SETTINGS[ 'service_url' ]
            self.redirect(redirect_url)


class queryURLData(authenticateBase):
    def get(self):
        userid=self.get_cookie_user()
        limit = int(self.get_argument("limit").encode('utf-8'))
        offset = int(self.get_argument("offset").encode('utf-8'))
        orderby = str(self.get_argument("sort").encode('utf-8'))
        ASC_DESC = self.get_argument("order").encode('utf-8').upper()
        #print limit,offset,orderby,ASC_DESC
        if(userid):
            mysql = mysqlLib()
            cnt= mysql.query_tbl_url_data_info_cnt()
            mysql.close()
            #print cnt
            mysql = mysqlLib()
            param = (orderby,ASC_DESC,offset,limit)
            ret = mysql.query_tbl_url_data_info(param)
            #print ret
            rows = []
            for item in ret:
                tmp_row = {}
                tmp_row['id'] = item[0]
                tmp_row['timepoint'] = str(item[1])
                tmp_row['accountName'] = item[2]
                tmp_row['totalurlNum'] = item[3]
                tmp_row['errorurlNum'] = item[4]
                tmp_row['deadDealNum'] = item[5]
                tmp_row['badDeadDealNum'] = item[6]
                tmp_row['openurlErrorNum'] = item[7]
                tmp_row['noListResultNum'] = item[8]
                tmp_row['errorCidNum'] = item[9]
                tmp_row['formatErrorNum'] = item[10]
                tmp_row['nullUrlNum'] = item[11]
                tmp_row['operation'] = item[0]
                rows.append(tmp_row)
            mysql.close()
            data = {"total":cnt,"rows":rows}
            self.write(json.dumps(data))
        else:
            redirect_url=CAS_SETTINGS[ 'cas_server' ] + '/login?service=' + CAS_SETTINGS[ 'service_url' ]
            self.redirect(redirect_url)

class queryUrlDetail(authenticateBase):
    def get(self):
        userid=self.get_cookie_user()
        urldataid = int(self.get_argument("urldataid").encode('utf-8'))
        if(userid):
            self.render("./plugins/3.urldata.html", usrname=userid,urldataid=urldataid)
        else:
            redirect_url=CAS_SETTINGS[ 'cas_server' ] + '/login?service=' + CAS_SETTINGS[ 'service_url' ]
            self.redirect(redirect_url)

class queryUrlDetailInfo(authenticateBase):
    def get(self):
        userid=self.get_cookie_user()
        urldataid = int(self.get_argument("urldataid").encode('utf-8'))
        limit = int(self.get_argument("limit").encode('utf-8'))
        offset = int(self.get_argument("offset").encode('utf-8'))
        orderby = str(self.get_argument("sort").encode('utf-8'))
        ASC_DESC = self.get_argument("order").encode('utf-8').upper()
        #print limit,offset,orderby,ASC_DESC,urldataid
        if(userid):
            mysql = mysqlLib()
            param=(urldataid)
            cnt= mysql.query_tbl_url_data_detail_info_cnt(param)
            mysql.close()
            #print cnt
            mysql = mysqlLib()
            param = (urldataid,orderby,ASC_DESC,offset,limit)
            ret = mysql.query_tbl_url_data_detail_info(param)
            #print ret
            rows = []
            if(len(ret) != 0):
                for item in ret:
                    tmp_row = {}
                    tmp_row['id'] = item[0]
                    tmp_row['accountname'] = item[1]
                    tmp_row['plan'] = item[2]
                    tmp_row['cell'] = item[3]
                    tmp_row['keyword'] = item[4]
                    tmp_row['discription'] = item[5]
                    tmp_row['url'] = item[6]
                    tmp_row['pc_mobile'] = item[7]
                    tmp_row['timepoint'] = str(item[8])
                    rows.append(tmp_row)
            mysql.close()
            data = {"total":cnt,"rows":rows}
            self.write(json.dumps(data))
        else:
            redirect_url=CAS_SETTINGS[ 'cas_server' ] + '/login?service=' + CAS_SETTINGS[ 'service_url' ]
            self.redirect(redirect_url)

class queryWordList(authenticateBase):
    def get(self):
        userid=self.get_cookie_user()
        if(userid):
            mysql = mysqlLib()
            param = ()
            ret = mysql.query_tbl_wordclass_data(param)
            rows = []
            for item in ret:
                rows.append(item[0])
            mysql.close()
            self.write(json.dumps(rows))
        else:
            redirect_url=CAS_SETTINGS[ 'cas_server' ] + '/login?service=' + CAS_SETTINGS[ 'service_url' ]
            self.redirect(redirect_url)

class queryWordInfo(authenticateBase):
    def post(self):
        post_param=urlparse.parse_qs(self.request.body,True)
        wordName=post_param['wordName'][0]
        startdate=post_param['startdate'][0]
        enddate=post_param['enddate'][0]
        param=(wordName, startdate, enddate)
        mysql=mysqlLib()
        ret = mysql.query_tbl_wordclass_data_info(param)
        ret_info = {}
        cat = []
        imp = []
        click = []
        cost = []
        for item in ret:
            cat.append(str(item[0]))
            imp.append(int(item[1]))
            click.append(int(item[2]))
            cost.append(float(item[3]))
        mysql.close()
        ret_info['cat'] = cat
        ret_info['imp'] = imp
        ret_info['click'] = click
        ret_info['cost'] = cost
        #print ret_info
        self.write(json.dumps(ret_info))

class queryMetricsAlarm(authenticateBase):
    def get(self):
        userid=self.get_cookie_user()
        metricsID = int(self.get_argument("metricsID").encode('utf-8'))
        if(userid):
            self.render("./plugins/alarm.html", usrname=userid,metricsID=metricsID)
        else:
            redirect_url=CAS_SETTINGS[ 'cas_server' ] + '/login?service=' + CAS_SETTINGS[ 'service_url' ]
            self.redirect(redirect_url)

class queryMetricsAlarmInfo(authenticateBase):
    def get(self):
        try:
            userid=self.get_cookie_user()
            metricsID = int(self.get_argument("metricsID").encode('utf-8'))
            limit = int(self.get_argument("limit").encode('utf-8'))
            offset = int(self.get_argument("offset").encode('utf-8'))
            orderby = str(self.get_argument("sort").encode('utf-8'))
            ASC_DESC = self.get_argument("order").encode('utf-8').upper()
            mysql = mysqlLib()
            param=(metricsID)
            cnt = mysql.query_tbl_alarmobj_metrics_related_cnt(param)
            mysql.close()

            mysql = mysqlLib()
            param=(metricsID,orderby,ASC_DESC,offset,limit)
            ret=mysql.query_tbl_alarmobj_metrics_related(param)

            rows = []
            if(len(ret) != 0):
                for item in ret:
                    tmp_row = {}
                    tmp_row['id'] = item[0]
                    tmp_row['description'] = item[1]
                    tmp_row['status'] = item[2]
                    tmp_row['datetime'] = str(item[3])
                    if(item[4] == None):
                        tmp_row['inactive_datetime'] = '-'
                    else:
                        tmp_row['inactive_datetime'] = str(item[4])
                    tmp_row['cause'] = item[5]
                    tmp_row['handleBy'] = item[6]
                    tmp_row['info'] = item[7]
                    tmp_row['operation'] = [item[0],item[2],str(item[5]),userid]
                    rows.append(tmp_row)
            mysql.close()
            data = {"total":cnt,"rows":rows}
            self.write(json.dumps(data))
        except Exception as e:
            logging.error(str(e))
            logging.info(traceback.print_exc())

class queryClickURLData(authenticateBase):
    def get(self):
        try:
            userid=self.get_cookie_user()
            #metricsID = int(self.get_argument("metricsID").encode('utf-8'))
            limit = int(self.get_argument("limit").encode('utf-8'))
            offset = int(self.get_argument("offset").encode('utf-8'))
            orderby = str(self.get_argument("sort").encode('utf-8'))
            ASC_DESC = self.get_argument("order").encode('utf-8').upper()

            mysql = mysqlLib()
            cnt = mysql.query_queryClickURLData_cnt()
            mysql.close()

            mysql = mysqlLib()
            param=(orderby,ASC_DESC,offset,limit)
            ret=mysql.query_queryClickURLData_info(param)

            rows = []
            if(len(ret) != 0):
                for item in ret:
                    info = json.loads(item[1])
                    for info_item in info:
                        tmp_row = {}
                        tmp_row['id'] = item[0]
                        try:
                            tmp_row['name'] = info_item['name']
                            tmp_row['expectURL'] = info_item['expLoc']
                            tmp_row['actURL'] = info_item['respLoc']
                            tmp_row['date'] = str(info_item['cutime'])
                        except Exception as e:
                            pass
                        rows.append(tmp_row)
            mysql.close()
            data = {"total":cnt,"rows":rows}
            self.write(json.dumps(data))
        except Exception as e:
            logging.error(str(e))
            logging.info(traceback.print_exc())

class queryCookieInfoData(authenticateBase):
    def get(self):
        try:
            userid=self.get_cookie_user()
            #metricsID = int(self.get_argument("metricsID").encode('utf-8'))
            limit = int(self.get_argument("limit").encode('utf-8'))
            offset = int(self.get_argument("offset").encode('utf-8'))
            orderby = str(self.get_argument("sort").encode('utf-8'))
            ASC_DESC = self.get_argument("order").encode('utf-8').upper()

            mysql = mysqlLib()
            cnt = mysql.query_queryCookieInfoData_cnt()
            mysql.close()

            mysql = mysqlLib()
            param=(orderby,ASC_DESC,offset,limit)
            ret=mysql.query_queryCookieInfoData_info(param)

            rows = []
            if(len(ret) != 0):
                for item in ret:
                    info = json.loads(item[1])
                    for info_item in info:
                        tmp_row = {}
                        tmp_row['id'] = item[0]
                        try:
                            tmp_row['name'] = info_item['name']
                            tmp_row['expCpsId'] = info_item['expCpsId']
                            tmp_row['resCpsId'] = info_item['resCpsId']
                            tmp_row['expCpsInfo'] = info_item['expCpsInfo']
                            tmp_row['resCpsInfo'] = info_item['resCpsInfo']
                            tmp_row['date'] = str(info_item['cutime'])
                        except Exception as e:
                            pass
                        rows.append(tmp_row)
            mysql.close()
            data = {"total":cnt,"rows":rows}
            self.write(json.dumps(data))
        except Exception as e:
            logging.error(str(e))
            logging.info(traceback.print_exc())

class queryVerifyInfoData(authenticateBase):
    def get(self):
        try:
            userid=self.get_cookie_user()
            #metricsID = int(self.get_argument("metricsID").encode('utf-8'))
            limit = int(self.get_argument("limit").encode('utf-8'))
            offset = int(self.get_argument("offset").encode('utf-8'))
            orderby = str(self.get_argument("sort").encode('utf-8'))
            ASC_DESC = self.get_argument("order").encode('utf-8').upper()

            mysql = mysqlLib()
            cnt = mysql.query_queryVerifyInfoData_cnt()
            mysql.close()

            mysql = mysqlLib()
            param=(orderby,ASC_DESC,offset,limit)
            ret=mysql.query_queryVerifyInfoData_info(param)

            rows = []
            if(len(ret) != 0):
                for item in ret:
                    try:
                        info = json.loads(item[1].strip("\""))
                    except Exception as e:
                        tmp_row = {}
                        tmp_row['id'] = item[0]
                        tmp_row['log'] = item[1].strip("\"")
                        tmp_row['operation'] = item[1].strip("\"")
                        rows.append(tmp_row)
            mysql.close()
            data = {"total":cnt,"rows":rows}
            self.write(json.dumps(data))
        except Exception as e:
            logging.error(str(e))
            logging.info(traceback.print_exc())

class queryPushSuccessInfoData(authenticateBase):
    def get(self):
        try:
            userid=self.get_cookie_user()
            #metricsID = int(self.get_argument("metricsID").encode('utf-8'))
            limit = int(self.get_argument("limit").encode('utf-8'))
            offset = int(self.get_argument("offset").encode('utf-8'))
            orderby = str(self.get_argument("sort").encode('utf-8'))
            ASC_DESC = self.get_argument("order").encode('utf-8').upper()

            mysql = mysqlLib()
            cnt = mysql.query_queryPushSuccessInfoData_cnt()
            mysql.close()

            mysql = mysqlLib()
            param=(orderby,ASC_DESC,offset,limit)
            ret=mysql.query_queryPushSuccessInfoData_info(param)

            rows = []
            if(len(ret) != 0):
                for item in ret:
                    info = json.loads(item[1])
                    tmp_row = {}
                    tmp_row['id'] = item[0]
                    try:
                        tmp_row['date'] = info['cutime']
                    except:
                        pass
                    tmp_row['totalSuccess'] = info['totalSuccess']
                    tmp_row['log'] = info['log']
                    tmp_row['operation'] = info['log']
                    rows.append(tmp_row)
            mysql.close()
            data = {"total":cnt,"rows":rows}
            self.write(json.dumps(data))
        except Exception as e:
            logging.error(str(e))
            logging.info(traceback.print_exc())

class queryPushFailInfoData(authenticateBase):
    def get(self):
        try:
            userid=self.get_cookie_user()
            #metricsID = int(self.get_argument("metricsID").encode('utf-8'))
            limit = int(self.get_argument("limit").encode('utf-8'))
            offset = int(self.get_argument("offset").encode('utf-8'))
            orderby = str(self.get_argument("sort").encode('utf-8'))
            ASC_DESC = self.get_argument("order").encode('utf-8').upper()

            mysql = mysqlLib()
            cnt = mysql.query_queryPushFailInfoData_cnt()
            mysql.close()

            mysql = mysqlLib()
            param=(orderby,ASC_DESC,offset,limit)
            ret=mysql.query_queryPushFailInfoData_info(param)

            rows = []
            if(len(ret) != 0):
                for item in ret:
                    info = json.loads(item[1])
                    tmp_row = {}
                    tmp_row['id'] = item[0]
                    try:
                        tmp_row['date'] = info['cutime']
                    except:
                        pass
                    tmp_row['totalFail'] = info['totalFail']
                    tmp_row['log'] = info['log']
                    tmp_row['operation'] = info['log']
                    rows.append(tmp_row)
            mysql.close()
            data = {"total":cnt,"rows":rows}
            self.write(json.dumps(data))
        except Exception as e:
            logging.error(str(e))
            logging.info(traceback.print_exc())

class query_tbl_zhixin_monitordata_hostlist(authenticateBase):
    def post(self):
        post_param=urlparse.parse_qs(self.request.body,True)
        flag = int(post_param['flag'][0])
        param=(flag)
        mysql=mysqlLib()
        ret = mysql.query_tbl_zhixin_monitordata_hostlist(param)
        hostlist = []
        for item in ret:
            hostlist.append(item[0])
        mysql.close()
        self.write(json.dumps(hostlist))

class queryzhixinDelayChartData(authenticateBase):
    def post(self):
        post_param=urlparse.parse_qs(self.request.body,True)
        startdate = post_param['startdate'][0]
        enddate = post_param['enddate'][0]
        hostname = post_param['hostname'][0]
        cityID = int(post_param['cityID'][0])
        srcID = int(post_param['srcID'][0])
        flag = int(post_param['flag'][0])
        param=(startdate, enddate, hostname, cityID, srcID, flag)
        mysql=mysqlLib()
        ret = mysql.query_tbl_zhixin_monitordata_delay(param)
        ret_info = {}
        cat = []
        as_delay = []
        zhixin_delay = []
        for item in ret:
            cat.append(str(item[0]))
            as_delay.append(float(item[1]))
            zhixin_delay.append(float(item[2]))
        mysql.close()
        ret_info['cat'] = cat
        ret_info['as_delay'] = as_delay
        ret_info['zhixin_delay'] = zhixin_delay
        self.write(json.dumps(ret_info))

class queryzhixinFlowChartData(authenticateBase):
    def post(self):
        post_param=urlparse.parse_qs(self.request.body,True)
        startdate = post_param['startdate'][0]
        enddate = post_param['enddate'][0]
        hostname = post_param['hostname'][0]
        cityID = int(post_param['cityID'][0])
        srcID = int(post_param['srcID'][0])
        flag = int(post_param['flag'][0])
        param=(startdate, enddate, hostname, cityID, srcID, flag)
        mysql=mysqlLib()
        ret = mysql.query_tbl_zhixin_monitordata_flow(param)
        ret_info = {}
        cat = []
        flow = []
        for item in ret:
            cat.append(str(item[0]))
            flow.append(int(item[1]))
        mysql.close()
        ret_info['cat'] = cat
        ret_info['flow'] = flow
        self.write(json.dumps(ret_info))

class queryzhixinNULLChartData(authenticateBase):
    def post(self):
        post_param=urlparse.parse_qs(self.request.body,True)
        startdate = post_param['startdate'][0]
        enddate = post_param['enddate'][0]
        hostname = post_param['hostname'][0]
        cityID = int(post_param['cityID'][0])
        srcID = int(post_param['srcID'][0])
        flag = int(post_param['flag'][0])
        param=(startdate, enddate, hostname, cityID, srcID, flag)
        mysql=mysqlLib()
        ret = mysql.query_tbl_zhixin_monitordata_null(param)
        ret_info = {}
        cat = []
        as_null = []
        zhixin_null = []
        for item in ret:
            cat.append(str(item[0]))
            as_null.append(int(item[1]))
            zhixin_null.append(int(item[2]))
        mysql.close()
        ret_info['cat'] = cat
        ret_info['as_null'] = as_null
        ret_info['zhixin_null'] = zhixin_null
        self.write(json.dumps(ret_info))

class querySEOTSMInterfaceInfo(authenticateBase):
    def post(self):
        post_param=urlparse.parse_qs(self.request.body,True)
        _type = post_param['type'][0]
        param=(_type)
        mysql=mysqlLib()
        ret = mysql.query_tbl_seo(param)
        data = []
        for item in ret:
            data.append(int(item[0]))
            data.append(int(item[1]))
            data.append(int(item[2]))
            data.append(json.loads(item[3]))
        mysql.close()
        self.write(json.dumps(data))



#########################################################################################
#########################################################################################
#########################################################################################
class serviceMonitor(authenticateBase):
    def get(self):
        userid=self.get_cookie_user()
        if(userid):
            self.render("./serviceMonitor/overallView.html",usrname=userid)
        else:
            redirect_url=CAS_SETTINGS[ 'cas_server' ] + '/login?service=' + CAS_SETTINGS[ 'service_url' ]
            self.redirect(redirect_url)
class historyAlarm(authenticateBase):
    def get(self):
        userid=self.get_cookie_user()
        if(userid):
            self.render("./serviceMonitor/historyAlarm.html",usrname=userid)
        else:
            redirect_url=CAS_SETTINGS[ 'cas_server' ] + '/login?service=' + CAS_SETTINGS[ 'service_url' ]
            self.redirect(redirect_url)
class queryAlarm(authenticateBase):
    def post(self):
        try:
            post_param=urlparse.parse_qs(self.request.body,True)
            limit=int(post_param['limit'][0])
            offset=int(post_param['offset'][0])

            param={"limit":limit,"offset":offset}
            mysql=mysqlLib()
            alarm_list=mysql.query_tbl_alarmobj(param)

            param={}
            alarm_totalcnt=mysql.query_alarm_totalcnt(param)
            mysql.close()

            alarm_list_info={}
            alarm_list_info['alarm_totalcnt']=alarm_totalcnt
            ret_dict=[]
            for index,item in enumerate(alarm_list):
                sub_ret_dict={}
                sub_ret_dict['id']=str(int(item[0]))
                sub_ret_dict['alarmConf_id']=str(int(item[1]))
                sub_ret_dict['monitorTask_id']=str(int(item[2]))
                sub_ret_dict['monitorObj_id']=str(int(item[3]))
                sub_ret_dict['monitorMetrics_id']=str(int(item[4]))
                sub_ret_dict['description']=item[5]
                sub_ret_dict['status']=str(int(item[6]))
                sub_ret_dict['datetime']=str(item[7])
                sub_ret_dict['cause']=item[8]
                sub_ret_dict['handleBy']=item[9]
                sub_ret_dict['info']=item[10]
                ret_dict.append(sub_ret_dict)
            alarm_list_info['ret_dict']=ret_dict
            self.write(json.dumps(alarm_list_info))
        except Exception as e:
            logging.error(str(e))
            logging.info(traceback.print_exc())
class queryMonitorTreeData(authenticateBase):
    def get(self):
        userid=self.get_cookie_user()
        if(userid):
            MonitorTreeData = parse_conf("./conf/bmeMonitorTree.json")
            self.write(json.dumps(MonitorTreeData))
        else:
            redirect_url=CAS_SETTINGS[ 'cas_server' ] + '/login?service=' + CAS_SETTINGS[ 'service_url' ]
            self.redirect(redirect_url)

################################################################################################################
class task(authenticateBase):
    def get(self):
        userid=self.get_cookie_user()
        task=self.get_argument("task").encode('utf-8')
        if(userid):
            self.render("./test/test.querytask.html",usrname=userid)
        else:
            redirect_url=CAS_SETTINGS[ 'cas_server' ] + '/login?service=' + CAS_SETTINGS[ 'service_url' ]
            self.redirect(redirect_url)

class conf(authenticateBase):
    def get(self):
        userid=self.get_cookie_user()
        conftype=self.get_argument("conftype").encode('utf-8')
        if(userid):
            if(conftype == "testsrv"):
                self.render("./conf/conf.testsrv.html",usrname=userid)
            elif(conftype == "testdata"):
                self.render("./conf/conf.testdata.html",usrname=userid)
            elif(conftype == "addsrv"):
                self.render("./conf/conf.addsrv.html",usrname=userid)
            elif(conftype == "adddata"):
                self.render("./conf/conf.adddata.html",usrname=userid)
            else:
                pass
        else:
            redirect_url=CAS_SETTINGS[ 'cas_server' ] + '/login?service=' + CAS_SETTINGS[ 'service_url' ]
            self.redirect(redirect_url)

class stat(authenticateBase):
    def get(self):
        userid=self.get_cookie_user()
        if(userid):
            self.render("./stat/stat.stat.html",usrname=userid)
        else:
            redirect_url=CAS_SETTINGS[ 'cas_server' ] + '/login?service=' + CAS_SETTINGS[ 'service_url' ]
            self.redirect(redirect_url)

class add_server(authenticateBase):
    def post(self):
        post_param=urlparse.parse_qs(self.request.body,True)
        name=post_param['name'][0]
        exenum=post_param['exenum'][0]
        ip=post_param['ip'][0]
        username=post_param['username'][0]
        password=post_param['password'][0]
        workspace=post_param['workspace'][0]
        belong=post_param['belong'][0]
        descpt=post_param['descpt'][0]

        param=(name,exenum,workspace,ip,username,password,belong,descpt)
        mysql=mysqlLib()
        n,last_id=mysql.add_server(param)
        mysql.close()
        ret_dict={"errcode":n}
        self.write(json.dumps(ret_dict))
class query_server(authenticateBase):
    def post(self):
        post_param=urlparse.parse_qs(self.request.body,True)
        limit=int(post_param['limit'][0])
        offset=int(post_param['offset'][0])
        #belong=post_param['belong'][0]

        param={"limit":limit,"offset":offset}
        mysql=mysqlLib()
        serverlist=mysql.query_server(param)

        param={}
        server_totalcnt=mysql.query_server_totalcnt(param)
        mysql.close()

        serverlist_info={}
        serverlist_info['server_totalcnt']=server_totalcnt
        ret_dict=[]
        for index,item in enumerate(serverlist):
            sub_ret_dict={}
            sub_ret_dict['id']=str(int(item[0]))
            sub_ret_dict['name']=item[1]
            sub_ret_dict['exenum']=str(int(item[2]))
            sub_ret_dict['workspace']=item[3]
            sub_ret_dict['ip']=item[4]
            sub_ret_dict['username']=item[5]
            sub_ret_dict['password']=item[6]
            sub_ret_dict['belong']=item[7]
            sub_ret_dict['descpt']=item[8]
            ret_dict.append(sub_ret_dict)
        serverlist_info['ret_dict']=ret_dict

        self.write(json.dumps(serverlist_info))

class query_server_workspace(authenticateBase):
    def post(self):
        post_param=urlparse.parse_qs(self.request.body,True)
        srv_id=int(post_param['id'][0])

        param={"id":srv_id}
        mysql=mysqlLib()
        serverlist=mysql.query_server(param)
        mysql.close()

        ret_dict={}
        workspace=serverlist[0][3]
        ret_dict['workspace']=workspace

        self.write(json.dumps(ret_dict))

class del_server(authenticateBase):
    def post(self):
        post_param=urlparse.parse_qs(self.request.body,True)
        server_id=post_param['id'][0]

        param=(server_id,)
        mysql=mysqlLib()
        n=mysql.del_server(param)
        mysql.close()
        ret_dict={"errcode":n}
        self.write(json.dumps(ret_dict))

class add_testdata(authenticateBase):
    def post(self):
        post_param=urlparse.parse_qs(self.request.body,True)
        datatype=post_param['type'][0]
        name=post_param['name'][0]
        belong=post_param['belong'][0]
        filenum=post_param['filenum'][0]
        descpt=post_param['desc'][0]

        param=(datatype,name,belong,filenum,descpt)
        mysql=mysqlLib()
        n,last_id=mysql.add_testdata(param)
        mysql.close()
        ret_dict={"errcode":n,"last_id":last_id}
        self.write(json.dumps(ret_dict))

class upload_testdata(authenticateBase):
    def post(self):
        post_param=urlparse.parse_qs(self.request.body,True)
        json_postdata={}
        try:
            for i in post_param[' name']:
                json_postdata[i.split("\r\n")[0].strip("\"")]=i.split("\r\n")[2]
        except Exception:
            pass
        #print json_postdata
        mysql=mysqlLib()
        param=(json_postdata['last_id'],self.request.files['Filedata'][0]['filename'],self.request.files['Filedata'][0]['body'])
        n,last_id=mysql.add_datastr(param)
        mysql.close()
        ret_dict={"errcode":n}
        self.write(json.dumps(ret_dict))

        '''file_dict_list = self.request.files['Filedata']
        for file_dict in file_dict_list:
            filename = file_dict["filename"]
            f = open("../proto/" + filename, "wb")
            f.write(file_dict["body"])
            f.close()
        sub_ret_dict={}
        ret=u"文件上传成功"
        sub_ret_dict['msg']=ret
        self.write(json.dumps(sub_ret_dict))'''

class download_testtool(authenticateBase):
    def post(self):
        post_param=urlparse.parse_qs(self.request.body,True)
        tooltype=post_param['tooltype'][0]
        proto=post_param['proto'][0]
        srv=post_param['srv'][0]
        path=post_param['path'][0]
        belong=post_param['belong'][0]
        cutime=datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")

        param=(tooltype,belong,cutime)
        mysql=mysqlLib()
        n,last_id=mysql.add_downloadstat(param)
        '''param={}
        downloadstat=mysql.query_downloadstat(1,param)
        print downloadstat
        downloadstat=mysql.query_downloadstat(0,param)
        print downloadstat'''
        mysql.close()

        if(int(tooltype) == 1 or int(tooltype) == 3):
            param={"testdata_id":proto}
            mysql=mysqlLib()
            datafilelist=mysql.query_datafile(param)
            mysql.close()
            for item in datafilelist:
                filename=item[0]
                filestr=item[1]
                #print filename
                #print filestr
                f = open("../proto/" + filename, "w")
                f.write(filestr)
                f.close()
            cmdstr="cd ../proto/ && ./build.sh"
            status,output=cmd_execute(cmdstr)
            cmdstr="cd .. && comake2 && make"
            status,output=cmd_execute(cmdstr)
            if(int(tooltype) == 1):
                cmdstr="cd .. && tar -czvf pb.tar.gz conf data log pbrpcbenchmark proto README"
                status,output=cmd_execute(cmdstr)
            if(int(tooltype) == 3):
                cmdstr="cd .. && tar -czvf pb.tar.gz case conf data log pbrpcclient pbunittest.py proto pub README"
                status,output=cmd_execute(cmdstr)

            param={"id":srv}
            mysql=mysqlLib()
            srvlist=mysql.query_server(param)
            ip=srvlist[0][2]
            username=srvlist[0][6]
            password=srvlist[0][7]
            #workspace=srvlist[0][3]
            mysql.close()
            rootdir="/home/users/yangjun03/protobuf/workspace/app-test/search/lbs-stat/upps_test/jenkinsFramework/protobuf/"
            filepath="pb.tar.gz"
            remotepath=path + "/pb/"
            ssh_cmd(ip,22,username,password,"mkdir -p " + remotepath)
            put_file(ip,22,username,password,rootdir+filepath,remotepath+"/"+filepath)
            ssh_cmd(ip,22,username,password,"cd " + remotepath + " && tar -xzvf " + filepath)
            #删除tar包
            ssh_cmd(ip,22,username,password,"cd " + remotepath + " && rm " + filepath)
            #删除所有.svn
            ssh_cmd(ip,22,username,password,"cd " + remotepath + " && find . -type d -name '.svn' | xargs rm -rf")

            sub_ret_dict={}
            ret=u"测试工具下载成功"
            sub_ret_dict['msg']=ret
            self.write(json.dumps(sub_ret_dict))
        else:
            if(int(tooltype) == 2):
                cmdstr="cd ~/httpclient/ && tar -czvf http.tar.gz conf data dep httpbenchmark.jar log README simplehttpserver.jar"
                status,output=cmd_execute(cmdstr)
            if(int(tooltype) == 4):
                cmdstr="cd ~/httpclient/ && tar -czvf http.tar.gz case com conf data dep httpclient.jar httpunittest.py log README simplehttpserver.jar"
                status,output=cmd_execute(cmdstr)

            param={"id":srv}
            mysql=mysqlLib()
            srvlist=mysql.query_server(param)
            ip=srvlist[0][2]
            username=srvlist[0][6]
            password=srvlist[0][7]
            #workspace=srvlist[0][3]
            mysql.close()
            rootdir="/home/users/yangjun03/httpclient/"
            filepath="http.tar.gz"
            remotepath=path + "/http/"
            ssh_cmd(ip,22,username,password,"mkdir -p " + remotepath)
            put_file(ip,22,username,password,rootdir+filepath,remotepath+"/"+filepath)
            ssh_cmd(ip,22,username,password,"cd " + remotepath + " && tar -xzvf " + filepath)
            #删除tar包
            ssh_cmd(ip,22,username,password,"cd " + remotepath + " && rm " + filepath)
            #删除所有.svn
            ssh_cmd(ip,22,username,password,"cd " + remotepath + " && find . -type d -name '.svn' | xargs rm -rf")

            sub_ret_dict={}
            ret=u"测试工具下载成功"
            sub_ret_dict['msg']=ret
            self.write(json.dumps(sub_ret_dict))

class query_downloadstat(authenticateBase):
    def post(self):
        param={}
        mysql=mysqlLib()
        downloadstat_week=mysql.query_downloadstat(1,param)
        downloadstat_all=mysql.query_downloadstat(0,param)
        mysql.close()

        datalist_info={}
        ret_dict=[]
        tmp = {}
        for index,item in enumerate(downloadstat_week):
            tmp[int(item[0])] = int(item[1])
        for i in xrange(1,5):
            if(i not in tmp):
                ret_dict.append(0)
            else:
                ret_dict.append(tmp[i])
        datalist_info['week']=ret_dict

        ret_dict=[]
        for index,item in enumerate(downloadstat_all):
            ret_dict.append(int(item[1]))
        datalist_info['all']=ret_dict

        self.write(json.dumps(datalist_info))

class del_testdata(authenticateBase):
    def post(self):
        post_param=urlparse.parse_qs(self.request.body,True)
        testdata_id=post_param['id'][0]

        param=(testdata_id,)
        mysql=mysqlLib()
        n=mysql.del_testdata(param)
        m=mysql.del_datafile(param)
        mysql.close()
        ret_dict={"errcoden":n,"errcodem":m}
        self.write(json.dumps(ret_dict))

class query_testdata(authenticateBase):
    def post(self):
        post_param=urlparse.parse_qs(self.request.body,True)
        limit=int(post_param['limit'][0])
        offset=int(post_param['offset'][0])
        belong=post_param['belong'][0]
        datatype=post_param['datatype'][0]

        if(datatype == -1):
            param={"belong":belong,"limit":limit,"offset":offset}
        else:
            param={"belong":belong,"type":datatype,"limit":limit,"offset":offset}
        mysql=mysqlLib()
        datalist=mysql.query_testdata(param)

        if(datatype == -1):
            param={"belong":belong}
        else:
            param={"belong":belong,"type":datatype}
        data_totalcnt=mysql.query_testdata_totalcnt(param)
        mysql.close()

        datalist_info={}
        datalist_info['data_totalcnt']=data_totalcnt
        ret_dict=[]
        for index,item in enumerate(datalist):
            sub_ret_dict={}
            sub_ret_dict['id']=str(int(item[0]))
            sub_ret_dict['name']=item[1]
            sub_ret_dict['type']=item[2]
            sub_ret_dict['belong']=item[3]
            sub_ret_dict['filenum']=item[4]
            sub_ret_dict['descpt']=item[5]
            ret_dict.append(sub_ret_dict)
        datalist_info['ret_dict']=ret_dict

        self.write(json.dumps(datalist_info))

class jobstatusubmit(tornado.web.RequestHandler):
    def post(self):
        try:
            post_param=urlparse.parse_qs(self.request.body,True)
            print post_param
            UserName=post_param['UserName'][0]
            ClusterName=post_param['ClusterName'][0]
            JenkinsURL = JENKINSURL
            if (ClusterName == "PublicCluster"):
                JenkinsURL = JENKINSURL
            else:
                ret_info = {"errcode":1, "ret":"ERROR : cluster not exist"}
                self.write(json.dumps(ret_info))
                return
            JobName=post_param['JobName'][0]
            SpecifyNode=int(post_param['SpecifyNode'][0])
            JobParameter=json.loads(post_param['JobParameter'][0])

            for item in JobParameter:
                if(type(JobParameter[item]) == list or type(JobParameter[item]) == dict):
                    JobParameter[item] = json.dumps(JobParameter[item])
            #print JobParameter
            url = gearmanjobclient.addtask(UserName, JenkinsURL, JobName, SpecifyNode, JobParameter)
            ret_info = {"errcode":0,"ret":url}
            self.write(json.dumps(ret_info))
        except KeyError:
            try:
                jsonobj = json.loads(self.request.body)
                UserName = jsonobj['UserName']
                ClusterName = jsonobj['ClusterName']
                JenkinsURL = JENKINSURL
                if (ClusterName == "PublicCluster"):
                    JenkinsURL = JENKINSURL
                else:
                    ret_info = {"errcode":1, "ret":"ERROR : cluster not exist"}
                    self.write(json.dumps(ret_info))
                    return
                JobName = jsonobj['JobName']
                SpecifyNode = int(jsonobj['SpecifyNode'])
                JobParameter = jsonobj['JobParameter']

                for item in JobParameter:
                    if(type(JobParameter[item]) == list or type(JobParameter[item]) == dict):
                        JobParameter[item] = json.dumps(JobParameter[item])
                #print JobParameter
                url = gearmanjobclient.addtask(UserName, JenkinsURL, JobName, SpecifyNode, JobParameter)
                ret_info = {"errcode":0,"ret":url}
                self.write(json.dumps(ret_info))
            except Exception as e:
                print(e)
                ret_info = {"errcode":1,"ret":"ERROR : internal error"}
                self.write(json.dumps(ret_info))

class query_nodes(tornado.web.RequestHandler):
    def post(self):
        try:
            jsonobj = json.loads(self.request.body)
            UserName = jsonobj['UserName']
            JenkinsURL = jsonobj['JenkinsURL']
            nodelist = querynodes.querynodes(JenkinsURL)
            print nodelist
            ret_info = {"ret":nodelist}
            self.write(json.dumps(ret_info))
        except Exception as e:
            print(e)
            ret_info = {"ret":"ERROR : internal error"}
            self.write(json.dumps(ret_info))

class jobstatus(tornado.web.RequestHandler):
    def post(self):
        #post_param=urlparse.parse_qs(self.request.body,True)
        #print self.request.body
        jsonobj = json.loads(self.request.body)
        unique_id = jsonobj['build']['parameters']['UNIQUE_ID']
        number = jsonobj['build']['number']
        phase = jsonobj['build']['phase']
        if (phase == "STARTED"):
            mysql = mysqlLib()
            param=(2, unique_id)
            mysql.update_task_status(param)
            print(u"#RUNNING, job running, 2")

            param=(number, unique_id)
            mysql.update_task_build_number(param)
            mysql.close()
        elif (phase == "FINALIZED" or phase == "COMPLETED"):
            status = jsonobj['build']['status']
            if (status == "SUCCESS"):
                mysql = mysqlLib()
                param=(3, unique_id)
                mysql.update_task_status(param)
                print(u"#SUCCESS, job complete, 3")
                mysql.close()
            elif (status == "ABORTED"):
                mysql = mysqlLib()
                param=(5, unique_id)
                mysql.update_task_status(param)
                print(u"#ABORTED, job aborted, 3")
                mysql.close()
            else:
                mysql = mysqlLib()
                param=(4, unique_id)
                mysql.update_task_status(param)
                print(u"#ERROR, job failed, 4")
                mysql.close()
        else:
            mysql = mysqlLib()
            param=(4, unique_id)
            mysql.update_task_status(param)
            print(u"#ERROR, job failed, 4")
            mysql.close()
    def get(self):
        unique_id = self.get_argument("job").encode('utf-8')
        param={"id":unique_id}
        mysql=mysqlLib()
        datalist=mysql.query_task(param)
        mysql.close()
        #print datalist
        datalist_info={}
        datalist_info['submit'] = datalist[0][1]
        datalist_info['url'] = datalist[0][2]
        datalist_info['jobname'] = datalist[0][3]
        datalist_info['status'] = datalist[0][5]
        datalist_info['build_number'] = datalist[0][6]
        #print datalist_info
        cmdstr = "curl " + datalist_info['url'] + "job/" + datalist_info['jobname'] + "/" + str(datalist_info['build_number']) + "/logText/progressiveText?start=0"
        #print cmdstr
        if (datalist_info['status'] == 3 or datalist_info['status'] == 4 or datalist_info['status'] == 5):
            status,output=cmd_execute(cmdstr)
            jobname = datalist_info['jobname']
            if (jobname == "pbdownload" or jobname == "addnode" or jobname == "delnode") :
                output = "INFO, task execute success."
            else:
                tmp = output.split("]'\r\n")[1].split("Notifying")[0]
                output = tmp
        else:
            output = "INFO, job is running now"
        datalist_info['output'] = output
        self.write(json.dumps(datalist_info))

class job_detail(authenticateBase):
    def get(self):
        userid=self.get_cookie_user()
        unique_id = self.get_argument("job").encode('utf-8')
        param={"id":unique_id}
        mysql=mysqlLib()
        datalist=mysql.query_task(param)
        mysql.close()
        #print datalist
        datalist_info={}
        datalist_info['submit'] = datalist[0][1]
        datalist_info['url'] = datalist[0][2]
        datalist_info['jobname'] = datalist[0][3]
        datalist_info['status'] = datalist[0][5]
        datalist_info['build_number'] = datalist[0][6]
        #print datalist_info
        cmdstr = "curl " + datalist_info['url'] + "job/" + datalist_info['jobname'] + "/" + str(datalist_info['build_number']) + "/logText/progressiveText?start=0"
        #print cmdstr
        if (datalist_info['status'] == 3 or datalist_info['status'] == 4 or datalist_info['status'] == 5):
            status,output=cmd_execute(cmdstr)
            jobname = datalist_info['jobname']
            if (jobname == "pbdownload" or jobname == "addnode" or jobname == "delnode") :
                output = "INFO, task execute success."
            else:
                tmp = output.split("]'\r\n")[1].split("Notifying")[0]
                output = tmp
                output = output.replace("\n","<br/>")
        else:
            output = "INFO, job is running now"
        datalist_info['output'] = output
        #self.write(json.dumps(datalist_info))

        if(userid):
            self.render("./taskmanagement/taskdetail.html",usrname=userid,datalist_info=datalist_info)
        else:
            redirect_url=CAS_SETTINGS[ 'cas_server' ] + '/login?service=' + CAS_SETTINGS[ 'service_url' ]
            self.redirect(redirect_url)

class jobstop(tornado.web.RequestHandler):
    def get(self):
        unique_id = self.get_argument("job").encode('utf-8')
        datalist_info = gearmanjobstop.gearmanjobstop(unique_id)
        print datalist_info
        self.write(json.dumps(datalist_info))

class query_task(authenticateBase):
    def post(self):
        post_param=urlparse.parse_qs(self.request.body,True)
        limit=int(post_param['limit'][0])
        offset=int(post_param['offset'][0])
        belong=post_param['belong'][0]

        param={"limit":limit,"offset":offset}
        mysql=mysqlLib()
        tasklist=mysql.query_task(param)

        param={}
        task_totalcnt=mysql.query_task_totalcnt(param)
        mysql.close()

        serverlist_info={}
        serverlist_info['task_totalcnt']=task_totalcnt
        ret_dict=[]
        for index,item in enumerate(tasklist):
            sub_ret_dict={}
            sub_ret_dict['id']=str(int(item[0]))
            sub_ret_dict['submit']=item[1]
            sub_ret_dict['jenkinsurl']=item[2]
            sub_ret_dict['jobname']=item[3]
            sub_ret_dict['build_params']=item[4]
            sub_ret_dict['status']=item[5]
            sub_ret_dict['build_number']=item[6]
            ret_dict.append(sub_ret_dict)
        serverlist_info['ret_dict']=ret_dict

        self.write(json.dumps(serverlist_info))

class add_task(authenticateBase):
    def get(self):
        userid=self.get_cookie_user()
        print userid
        if(userid):
            self.render("./taskmanagement/addtask.html",usrname=userid)
        else:
            redirect_url=CAS_SETTINGS[ 'cas_server' ] + '/login?service=' + CAS_SETTINGS[ 'service_url' ]
            self.redirect(redirect_url)

class query_node(authenticateBase):
    def get(self):
        userid=self.get_cookie_user()
        if(userid):
            self.render("./nodemanagement/nodemanagement.html",usrname=userid)
        else:
            redirect_url=CAS_SETTINGS[ 'cas_server' ] + '/login?service=' + CAS_SETTINGS[ 'service_url' ]
            self.redirect(redirect_url)

class add_node(authenticateBase):
    def get(self):
        userid=self.get_cookie_user()
        if(userid):
            self.render("./nodemanagement/addnode.html",usrname=userid)
        else:
            redirect_url=CAS_SETTINGS[ 'cas_server' ] + '/login?service=' + CAS_SETTINGS[ 'service_url' ]
            self.redirect(redirect_url)

class nextstep(authenticateBase):
    def get(self):
        userid=self.get_cookie_user()
        service_type = int(self.get_argument("type").encode('utf-8'))
        JenkinsURL = JENKINSURL
        nodelist = querynodes.querynodes(JenkinsURL)
        if(userid):
            if(service_type == 1):
                self.render("./taskmanagement/nextstop_pbdownload.html",usrname=userid,nodelist=nodelist)
            if(service_type == 2):
                self.render("./taskmanagement/nextstop_pbclient.html",usrname=userid,nodelist=nodelist)
            if(service_type == 3):
                self.render("./taskmanagement/nextstop_pbbenchmark.html",usrname=userid,nodelist=nodelist)
        else:
            redirect_url=CAS_SETTINGS[ 'cas_server' ] + '/login?service=' + CAS_SETTINGS[ 'service_url' ]
            self.redirect(redirect_url)

class family(authenticateBase):
    def get(self):
        userid=self.get_cookie_user()
        print userid
        if(userid):
            self.render("pb.html",usrname=userid)
        else:
            redirect_url=CAS_SETTINGS[ 'cas_server' ] + '/login?service=' + CAS_SETTINGS[ 'service_url' ]
            self.redirect(redirect_url)

if __name__ == "__main__":
    settings={"template_path": os.path.join(os.path.dirname(__file__), "template") ,
    "static_path": os.path.join(os.path.dirname(__file__), "static") ,
    "debug":False,
    "cookie_secret":"61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo="}
    define("port", default=defaultport, help="run on the given port", type=int)

    tornado.options.parse_command_line()
    app=tornado.web.Application(handlers=[
    ( r'/pb/task/', task),
    ( r'/pb/conf/', conf),
    ( r'/pb/stat/', stat),
    ( r'/pb/add_server/', add_server),
    ( r'/pb/query_server/', query_server),
    ( r'/pb/del_server/', del_server),
    ( r'/pb/query_server_workspace/', query_server_workspace),
    ( r'/pb/add_testdata/', add_testdata),
    ( r'/pb/upload_testdata/', upload_testdata),
    ( r'/pb/query_testdata/', query_testdata),
    ( r'/pb/del_testdata/', del_testdata),
    ( r'/pb/download_testtool/', download_testtool),
    ( r'/pb/query_downloadstat/', query_downloadstat),

    ( r'/', LoginHandler),
    ( r'/logout/',LogoutHandler),
    ( r'/serviceMonitor/',serviceMonitor),
    ( r'/serviceMonitor/historyAlarm/',historyAlarm),
    ( r'/serviceMonitor/queryAlarm/',queryAlarm),
    ( r'/serviceMonitor/queryMonitorTreeData/',queryMonitorTreeData),

    ( r'/jobsubmit/',jobstatusubmit),
    ( r'/jobstatus/',jobstatus),
    ( r'/job_detail/',job_detail),
    ( r'/jobstop/',jobstop),
    ( r'/querynodes/',query_nodes),

    ( r'/addtask/', add_task),
    ( r'/query_task/', query_task),
    ( r'/node/',query_node),
    ( r'/addnode/',add_node),
    ( r'/nextstep/',nextstep),

    ( r'/family/',family),
    ( r'/stat/', stat),

    ( r'/nav/', nav),
    ( r'/monitor/', monitor),
    ( r'/help/', helpcls),
    ( r'/querytreedata/', querytreedata),
    ( r'/queryMonitorMetricsData/', queryMonitorMetricsData),
    ( r'/queryAlarmDayperiod/', queryAlarmDayperiod),
    ( r'/queryHistoryAlarm/', queryHistoryAlarm),
    ( r'/queryAlarmDetail/', queryAlarmDetail),
    ( r'/updateAlarmInfo/', updateAlarmInfo),
    ( r'/queryMetricsDataChart/', queryMetricsDataChart),
    ( r'/queryAccountList/',queryAccountList),
    ( r'/queryAccountList_Click/',queryAccountList_Click),
    ( r'/queryAccountBalance/',queryAccountBalance),
    ( r'/queryAccountClick/',queryAccountClick),
    ( r'/queryAccounts/',queryAccounts),
    ( r'/queryTableData/',queryTableData),
    ( r'/queryURLData/',queryURLData),
    ( r'/queryUrlDetail/',queryUrlDetail),
    ( r'/queryUrlDetailInfo/',queryUrlDetailInfo),
    ( r'/queryWordList/',queryWordList),
    ( r'/queryWordInfo/',queryWordInfo),
    ( r'/queryMetricsAlarm/',queryMetricsAlarm),
    ( r'/queryMetricsAlarmInfo/',queryMetricsAlarmInfo),
    ( r'/queryClickURLData/',queryClickURLData),
    ( r'/queryCookieInfoData/',queryCookieInfoData),
    ( r'/queryVerifyInfoData/',queryVerifyInfoData),
    ( r'/queryPushSuccessInfoData/',queryPushSuccessInfoData),
    ( r'/queryPushFailInfoData/',queryPushFailInfoData),
    ( r'/query_tbl_zhixin_monitordata_hostlist/',query_tbl_zhixin_monitordata_hostlist),
    ( r'/queryzhixinDelayChartData/',queryzhixinDelayChartData),
    ( r'/queryzhixinFlowChartData/',queryzhixinFlowChartData),
    ( r'/queryzhixinNULLChartData/',queryzhixinNULLChartData),
    ( r'/querySEOTSMInterfaceInfo/',querySEOTSMInterfaceInfo),



    ],**settings
    )
    HttpServer=tornado.httpserver.HTTPServer(app)
    HttpServer.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

