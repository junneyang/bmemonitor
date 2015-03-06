#-*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        获取给定日期的词类的 展现量  点击量  消费，并入库
# Purpose:
#
# Author:      caolei07
#
# Created:     21/01/2015
# Copyright:   (c) caolei07 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import suds
import traceback as tb
import sys
import time
import string
import urllib2
import urllib
import httplib
from urllib2 import Request, URLError, HTTPError
import xlwt
import re
import os
import psutil
import threading
import time
import datetime
import traceback
from statpy.BeautifulSoup import BeautifulSoup
from statpy.sms_v3_CampaignService import *
from statpy.sms_v3_AdgroupService import *
from statpy.sms_v3_KeywordService import *
from statpy.sms_v3_RankService import *
from statpy.sms_v3_ReportService import *
from accountinfo import *
from com.mysqlLib import *
import smtplib
import commands

#GetReport需要的密码
password="Nuomi20131127"

class WordCalss:
    def __init__(self,check_date):
        self.check_date = check_date
        self.accountInfo = list()
        self.collect_dict = dict()

    def main(self):
        #1.获取账户信息
        mysql = AccountInfo()
        self.accountInfo =mysql.get_tbl_accountinfo()
        mysql.save_tbl_accountinfo()
        mysql.save_tbl_cid()
        #2. 依次检查每一个账户
        index = 0
        while(index<len(self.accountInfo)):
            keyword = self.GetReport(self.check_date, self.accountInfo[index])
            each_dict = self.CheckKeyWordByAccount(self.accountInfo[index],keyword)
            self.addCollect(each_dict)
            index+=1
            print index

        #3. 写入数据库
        mysql = mysqlLib()
        ret_list = list()
        for key in self.collect_dict:
            param=[self.check_date,key.encode('UTF-8'),self.collect_dict[key][0],self.collect_dict[key][1],self.collect_dict[key][2]]
            mysql.add_wordclass_data(param)
            ret_list.append(param)
        mysql.close()
        print u'end'
        return ret_list

    def addCollect(self,each_dict):
        for key in each_dict:
        #需要对key进行替换
            tmp = self.solveKey(key.decode('GBK'))
            if len(self.collect_dict)==0:
                self.collect_dict[tmp] = each_dict[key]
                continue
            if self.collect_dict.has_key(tmp):
                self.collect_dict[tmp] = self.add_list(self.collect_dict[tmp],each_dict[key])
            else:
                self.collect_dict[tmp] = each_dict[key]

    def solveKey(self,input):
        print input
        if('wise_品牌词_sub品类词' in input):
            return 'wise_品牌词_sub品类词'
        if('pc_品牌词_sub品类词' in input):
            return 'pc_品牌词_sub品类词'
        if('wise_泛需求_range' in input):
            return 'wise_泛需求_range'
        if('pc_泛需求_range' in input):
            return 'pc_泛需求_range'
        if('wise_泛需求_district' in input):
            return 'wise_泛需求_district'
        if('pc_泛需求_district' in input):
            return 'pc_泛需求_district'
        if('wise_泛需求_city' in input):
            return 'wise_泛需求_city'
        if('pc_泛需求_city' in input):
            return 'pc_泛需求_city'
        if('wise_多城市非美食_Brand' in input):
            return 'wise_多城市非美食_Brand'
        if('pc_多城市非美食_brand' in input):
            return 'pc_多城市非美食_brand'
        if('wise_北京非美食_Brand' in input):
            return 'wise_北京非美食_Brand'
        if('pc_北京非美食_brand' in input):
            return 'pc_北京非美食_brand'
        if('wise_北京_电影_brand' in input):
            return 'wise_北京_电影_brand'
        if('pc_北京_电影_brand' in input):
            return 'pc_北京_电影_brand'
        if('wise_多城市_电影_brand' in input):
            return 'wise_多城市_电影_brand'
        if('pc_多城市_电影_brand' in input):
            return 'pc_多城市_电影_brand'

        textLine = input.split('_')
        ret = textLine
        if(textLine[-1].isdigit()):
            ret = textLine[0:-1]
        if(ret[0]=='闪投'):
            ret = ret[1:]
        output =""
        for item in ret:
            output+=str(item)+"_"
        return output[:-1]

    def add_list(self,list1,list2):
        if(len(list1)!=len(list2)):
            return 0
        i=0
        c=list()
        while(i<len(list1)):
            c.append(list1[i]+list2[i])
            i+=1
        return c

    def GetReport(self, strTime, accountInfo):
            keywordshow = list()
            try:
                if accountInfo[0] == "baidu-短语商家2140114":
                    self.password = "Ab1234567890"
                else:
                    self.password = "Nuomi20131127"

                service = sms_v3_ReportService()
                service.setUsername(accountInfo[0])
                service.setPassword(self.password)
                service.setToken("796fbec57ff499a2894ea4ac0b579c1b")
                strStartDate = strTime + 'T' + '00:00:00.000'
                strEndDate = strTime + 'T' + '23:59:59.000'
                print strStartDate, strEndDate
                #获取关键词报告，参数表示日报
                request = {"reportRequestType":{"performanceData":["impression","click","cost"], "startDate" : strStartDate, "endDate" : strEndDate, "levelOfDetails" : 11, "idOnly": 0, "reportType" : 14,"statRange":2,"attributes":None,"statIds":None,"unitOfTime":5, "device":0}}
                getProfessionalReportIdResp = service.getProfessionalReportId(request)
                print getProfessionalReportIdResp
                getNum = 0
                while getProfessionalReportIdResp is None:
                        time.sleep(1)
                        if(getNum > 20):
                                break
                        getNum +=1
                        getProfessionalReportIdResp = service.getProfessionalReportId(request)
                        print getProfessionalReportIdResp

                if (getProfessionalReportIdResp == None):
                        print "Get Professional Report Id fail!"
                        return None
                getNum = 0
                while True :
                        print "Get the report id response \n"
                        time.sleep(5)
                        if(getNum > 24):
                                return ''
                        getNum +=1
                        reportId = {"reportId": getProfessionalReportIdResp["body"]["reportId"]};
                        getReportStateResp = service.getReportState(reportId)
                        print getReportStateResp
                        getReportStatNum = 0
                        while getReportStateResp is None or getReportStateResp["body"] is None or getReportStateResp["body"]["isGenerated"] is None:
                            time.sleep(1)
                            if getReportStatNum > 10:
                                return None
                            getReportStatNum += 1
                            getReportStateResp = service.getReportState(reportId)
                            print getReportStateResp

                        if (getReportStateResp["body"]["isGenerated"] == 3 ):
                                print "Get the report state success\n"
                                reportFilePath = service.getReportFileUrl(reportId)
                                print reportFilePath
                                reportFileNum =0
                                while reportFilePath is None or reportFilePath["body"] is None or reportFilePath["body"]["reportFilePath"] is None:
                                    if reportFileNum > 10:
                                        return 0
                                    reportFileNum += 1
                                    reportFilePath = service.getReportFileUrl(reportId)
                                    print reportFilePath
                                url = reportFilePath["body"]["reportFilePath"]
                                #r = requests.get(url);
                                #strText = r.content
                                f = urllib2.urlopen(url)
                                strText = f.read()
                                textLine = strText.split('\n')
                                i = 0
                                for info in textLine:
                                    if(i == 0):
                                        i = 1
                                        continue
                                    keywordshow.append(info)
                                break

            except Exception, e:
                print e
                tb.print_exc()
            return keywordshow

    def CheckKeyWordByAccount(self, accountInfo,keywordlist):
        strUserName = accountInfo[0]
        if accountInfo[0] == "baidu-短语商家2140114":
            self.password = "Ab1234567890"
        else:
            self.password = "Nuomi20131127"
        keyworkClient = sms_v3_KeywordService()
        keyworkClient.setUsername(accountInfo[0])
        keyworkClient.setPassword(self.password)
        keyworkClient.setToken("796fbec57ff499a2894ea4ac0b579c1b")

        adGroupClient = sms_v3_AdgroupService()
        adGroupClient.setUsername(accountInfo[0])
        adGroupClient.setPassword(self.password)
        adGroupClient.setToken("796fbec57ff499a2894ea4ac0b579c1b")

        indexNum = 0
        repeategroupNum = 0
        usefulgroupNum = 0

        groupIdDict = dict()
        for keywordinfo in keywordlist:
            if(cmp(keywordinfo, '') == 0):
                continue
            textList = keywordinfo.split('\t')

            impression=float(textList[10])
            click=float(textList[11])
            tmp=textList[12].split('\\')[0]
            cost=float(tmp)
            tmpp=[impression,click,cost]
            if groupIdDict.has_key(textList[4]):
                groupIdDict[textList[4]] = self.add_list(groupIdDict[textList[4]],tmpp)
                continue
            else:
                groupIdDict[textList[4]] = tmpp
        return groupIdDict
if __name__ == '__main__':
    check_date = sys.argv[1]
    myWordCalss = WordCalss(check_date)
    myWordCalss.main()
