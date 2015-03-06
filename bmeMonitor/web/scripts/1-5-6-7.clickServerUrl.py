#-*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        cps clickServer 链接跳转 监控
# Purpose:
#
# Author:      caolei07
#
# Created:     21/01/2015
# Copyright:   (c) caolei07 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import sys
import time
import datetime
sys.path.append('../')
from com.logLib import *
from com.confLib import *
from com.cmdLib import *
from Monitor import Monitor
from com.mysqlLib import *
import Cookie
import httplib
import urllib

import TestConf

def exec_case(client, aCase, fout):
    ret_dict = dict()
    reqUrl = aCase['url']
    expLoc = aCase['location']

    print >> fout, '请求参数 = %s' % reqUrl
    print >> fout, '预期跳转 = %s' % expLoc
    ret_dict['name'] = aCase['name']
    ret_dict['expLoc'] = expLoc

    if aCase.has_key('cps_id'):
        print >> fout, '预期CPSID = %d' % aCase['cps_id']
        ret_dict['expCpsId'] = aCase['cps_id']
    if aCase.has_key('cps_info'):
        print >> fout , '预期CPSInfo = %s' % aCase['cps_info']
        ret_dict['expCpsInfo'] = aCase['cps_info']
    print >> fout, ''

    client.request('GET', reqUrl)
    resp = client.getresponse()
    try:
        if  resp:
            print >> fout, '返回状态 = %d' % resp.status
            # BES 需要经过二次跳转，无Cookie
            if aCase['name'] == 'BES' :
                midLoc = resp.getheader('location')
                print >> fout, '中间跳转 = %s' % midLoc
                for hd in resp.getheaders():
                    print >> fout, hd
                midHost, midUrl = urllib.splithost(urllib.splittype(midLoc)[1])
                midClient = httplib.HTTPConnection(midHost)
                midClient.request('GET', midUrl)
                midResp = midClient.getresponse()

                print >> fout, '最终状态 = %d' % midResp.status
                respLoc = midResp.getheader('location')
                for hd in midResp.getheaders():
                    print >> fout, hd
                print >> fout, '最终跳转 = %s' % respLoc
                ret_dict['respLoc'] = respLoc
                print >> fout, respLoc == expLoc
                print >> fout, ''


            # 晶赞拼接URL即可，无cookie写入
            elif aCase['name'] == 'zamplus':
                respLoc = resp.getheader('location')
                print >> fout, '最终跳转 = %s' % respLoc
                for hd in resp.getheaders():
                    print >> fout, hd
                print >> fout, respLoc == expLoc
                print >> fout, ''
                ret_dict['respLoc'] = respLoc

            else:
                # 其他渠道 查看跳转信息和 Cookie设置信息
                for hd in resp.getheaders():
                    print >> fout, hd
                respLoc = resp.getheader('location')
                print >> fout, '最终跳转 = %s' % respLoc
                print >> fout, respLoc == expLoc

                cookie = Cookie.SimpleCookie()
                cookie.load(resp.getheader('Set-Cookie'))
                cps_id = cookie['CPS_COOKIE_NAME'].value
                cps_info = urllib.unquote(cookie['nm_cps_info'].value)
                print >> fout, 'Set-Cookie : CPS_COOKIE_NAME = %s  \tnm_cps_info = %s ' % (cps_id, cps_info)
                ret_dict['respLoc'] = respLoc
                ret_dict['cookie'] = cookie
                ret_dict['resCpsId'] = cps_id
                ret_dict['resCpsInfo'] = cps_info
        else:
            print >> fout, 'No response'
    except Exception as err:
        print >> fout, 'Error and No response'
        print >> fout, err
    print >> fout, ''

    return ret_dict


class myMonitor(Monitor):
    def __init__(self, log_file, last_id, monitorObj_id, monitorMetrics_id, monitorMetrics_name):
        Monitor.__init__(self, log_file, last_id, monitorObj_id, monitorMetrics_id, monitorMetrics_name)
        self.dataList = list()
        self.warnList = list()
    #获取监控数据、上报告警等，此部分由具体子类改写实现。
    def monitor_alarm_proc(self):
        logging.info("task  task_id:" + str(self.last_id) + " monitor_alarm_proc start")
        cutime=datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")

        result_file = 'test_result.txt'
        resOut = open(result_file, 'w')

        #step1: 调用cps接口
        caseCollection = TestConf.TEST_URL_LIST
        host = TestConf.TEST_SERVER['host']
        port = TestConf.TEST_SERVER['port']
        currIdx = 0
        data_list = list()
        for aCase in caseCollection:
            client = httplib.HTTPConnection(host, port)
            print 'Execute Case %d  ...' % currIdx
            #返回跳转链接，和cookie
            tmpdict = exec_case(client, aCase, resOut)
            data_list.append(tmpdict)
            currIdx += 1
            resOut.flush()
        resOut.close()

        #step2: 检查
        for item in data_list:
            each_data = {}
            each_data['name']=str(item['name'])
            if item.has_key('respLoc') and item.has_key('expLoc'):
                each_data['respLoc']=item['respLoc']
                each_data['expLoc']=item['expLoc']
                each_data['cutime']=cutime
                if item['expLoc']!=item['respLoc']:
                    dsc = '商家【'+str(item['name'])+'】：链接跳转出错，预期：'+str(item['expLoc'])+"，实际："+str(item['respLoc'])
                    self.warnList.append(dsc)
            elif not item.has_key('expLoc'):
                dsc = '商家【'+str(item['name'])+'】：链接跳转出错，请给出预期跳转链接。'
                self.warnList.append(dsc)
            elif not item.has_key('respLoc'):
                dsc = '商家【'+str(item['name'])+'】：链接跳转出错，预期：'+str(item['expLoc'])+"，实际跳转失败，无地址"
                self.warnList.append(dsc)

            """
            if item['name']=='BES' or item['name']=='zamplus':
                print str(item['name'])+'无cookie'
                continue

            if item.has_key('resCpsId') and item.has_key('expCpsId'):
                each_data['resCpsId']=item['resCpsId']
                each_data['expCpsId']=item['expCpsId']
                if str(item['expCpsId'])!=str(item['resCpsId']):
                    dsc = '商家【'+str(item['name'])+'】：cpsid 不一致，预期:'+str(item['expCpsId'])+"，实际:"+str(item['resCpsId'])
                    self.warnList.append(dsc)
            else:
                dsc = '商家【'+str(item['name'])+'】：cpsid 不一致'
                self.warnList.append(dsc)

            if item.has_key('resCpsInfo') and item.has_key('expCpsInfo'):
                each_data['resCpsInfo']=item['resCpsInfo']
                each_data['expCpsInfo']=item['expCpsInfo']
                if not self.check_cps_info(item['expCpsInfo'],item['resCpsInfo']):
                    dsc = '商家【'+str(item['name'])+'】：cps_info 不一致，预期:'+str(item['expCpsInfo'])+"，实际:"+str(item['resCpsInfo'])
                    self.warnList.append(dsc)
            else:
                dsc = '商家【'+str(item['name'])+'】：cps_info 不一致'
                self.warnList.append(dsc)
            """
            self.dataList.append(each_data)
        print u'end'

        #存入本地数据库
        self.add_monitor_data(self.last_id, 0, self.dataList)
        logging.info("task  task_id:" + str(self.last_id) + " insert into tbl_monitordata end")

        #查询报警配置
        alarm_conf_id,monitorObj_id,monitorMetrics_id,name,description,status,conf = self.query_alarm_conf(self.monitorObj_id, self.monitorMetrics_id)
        for item in self.warnList:
            #####################################添加告警，暂时屏蔽-by yangjun03############################################################
            #self.add_alarm(alarm_conf_id, self.last_id, monitorObj_id,monitorMetrics_id, description+" "+str(item) , 0, cutime)
            #####################################添加告警，暂时屏蔽-by yangjun03############################################################
            self.mail_send(self.subject+" "+description, str(item), self.from_mail_addr, self.to_mail_addr, self.mail_server)
            self.msgSend(self.phone_list, str(item) , mode="qapi")

    def check_cps_info(self,exp,res):
        dict1 = eval(exp)
        dict2 = eval(res)
        for k,v in dict1.iteritems():
            if dict2.has_key(k):
                if str(v)!=str(dict2[k]):
                    return False
            else:
                return False
        return True

if __name__ == "__main__":
    log_file = "./log/" + sys.argv[0] + ".log"
    last_id = sys.argv[1]
    monitorObj_id = sys.argv[2]
    monitorMetrics_id = sys.argv[3]
    monitorMetrics_name = sys.argv[4]
    log_init(log_file)
    mymonitor = myMonitor(log_file, last_id, monitorObj_id, monitorMetrics_id, monitorMetrics_name)
    mymonitor.start()
