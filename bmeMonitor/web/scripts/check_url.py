#-*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        url 监控 子线程
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
import smtplib
import commands
from com.mysqlLib import *
strUserName = ''

class MyUrlMonitor(threading.Thread):
    def __init__(self,dateStr,accountInfo,taskid):
        threading.Thread.__init__(self)
        self.taskid = taskid
        self.dateStr = dateStr
        self.accountInfo= accountInfo
        self.keywordshow = list()
        self.groupIdDict = {}
        self.urlList = list()
        self.mobileurlNum = 0
        self.pcurlNum = 0
        #每种url的数量
        self.pcdealinfoNum = 0
        self.pcrepeatetinyurlNum = 0
        self.mobiledealinfoNum = 0
        self.mobilerepeatetinyurlNum = 0
        self.searchurlNum = 0
        self.pcdeallistNum = 0
        self.otherurlsampleNum = 0
        self.pcothercatgoryurlNum = 0
        self.totalurlNum = 0
        self.errorurlNum = 0
        self.formatErrorNum = 0
        self.openurlErrorNum = 0
        self.noListResultNum = 0
        self.errorCidNum = 0
        self.deadDealNum = 0
        self.badDeadDealNum = 0
        self.readurlNum = 0
        self.nullUrlNum = 0
        #存储每一个用户详细信息的
        self.intFlag = 0#0:file0, 1:file1 2:file2
        self.resList = list()
        self.openurltimeout = 10
        self.sampleValue = 1
        self.sampleSeed = 3
        self.sampleValueMobile = 1
        self.sampleSeedMobile = 3
        self.pctiny_url = {}
        self.mobiletiny_url = {}
        self.accountCid = {}
        self.deadDeal = {}

    def run(self):
        print '*********************************'
        print self.taskid
        self.LoadAccountCid('accountinfoAllCid.txt')
        self.LoadDeadDeal('deadtinyurl.txt')
        #得到账户的关键词情况，日报
        self.GetReport(self.dateStr, self.accountInfo)
        #对每一个关键字检查对应的url,写入self.urlList
        self.CheckKeyWord(self.accountInfo)

        #统计数据存入本地数据库
        mysql = mysqlLib()
        param=[self.taskid,self.dateStr,self.accountInfo[0],self.totalurlNum,self.errorurlNum,self.deadDealNum,self.badDeadDealNum,self.openurlErrorNum,self.noListResultNum,self.errorCidNum,self.formatErrorNum,self.nullUrlNum]
        mysql.add_url_data(param)

        #详细情况存入本地数据库
        #1.得到tbl_url_data的id
        accountName=self.accountInfo[0]
        param=[accountName,self.dateStr]
        id=mysql.get_url_data_id(param)
        #2.插入tbl_errorurl
        for listInfo in self.resList:
            if(len(listInfo) <= 0):
                continue
            param=[id,self.accountInfo[0],listInfo[2],listInfo[3],listInfo[4],listInfo[5],listInfo[7],listInfo[6],self.dateStr]
            mysql.add_urlerror_data(param)

        print '***'
        mysql.close()

    def GetReport(self, strTime, accountInfo):
            try:
                if accountInfo[0] == "baidu-短语商家2140114":
                    self.password = "Ab1234567890"
                else:
                    self.password = "Nuomi20131127"

                service = sms_v3_ReportService()
                service.setUsername(accountInfo[0])
                service.setPassword(self.password)
                service.setToken(accountInfo[1])
                strStartDate = strTime + 'T' + '00:00:00.000'
                strEndDate = strTime + 'T' + '23:59:59.000'
                print strStartDate, strEndDate
                request = {"reportRequestType":{"performanceData":["click","impression"], "startDate" : strStartDate, "endDate" : strEndDate, "levelOfDetails" : 11, "idOnly": 0, "reportType" : 14,"statRange":2,"attributes":None,"statIds":None,"unitOfTime":5, "device":0}}
                getProfessionalReportIdResp = service.getProfessionalReportId(request)
                getNum = 0
                while getProfessionalReportIdResp is None:
                        time.sleep(1)
                        if(getNum > 20):
                                break
                        getNum +=1
                        getProfessionalReportIdResp = service.getProfessionalReportId(request)

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
                        getReportStatNum = 0
                        while getReportStateResp is None or getReportStateResp["body"] is None or getReportStateResp["body"]["isGenerated"] is None:
                            time.sleep(1)
                            if getReportStatNum > 10:
                                return None
                            getReportStatNum += 1
                            getReportStateResp = service.getReportState(reportId)

                        if (getReportStateResp["body"]["isGenerated"] == 3 ):
                                print "Get the report state success\n"
                                reportFilePath = service.getReportFileUrl(reportId)
                                reportFileNum =0
                                while reportFilePath is None or reportFilePath["body"] is None or reportFilePath["body"]["reportFilePath"] is None:
                                    if reportFileNum > 10:
                                        return 0
                                    reportFileNum += 1
                                    reportFilePath = service.getReportFileUrl(reportId)
                                url = reportFilePath["body"]["reportFilePath"]
                                f = urllib2.urlopen(url)
                                strText = f.read()
                                textLine = strText.split('\n')
                                i = 0
                                for info in textLine:
                                    if(i == 0):
                                        i = 1
                                        continue
                                    self.keywordshow.append(info.decode('gb2312'))
                                break
            except Exception, e:
                print e
                tb.print_exc()

    def CheckKeyWord(self, accountInfo):
        newAccount = list()
        for item in accountInfo:
            newAccount.append(str(item).encode('utf-8'))

        strUserName = newAccount[0]
        if newAccount[0] == "baidu-短语商家2140114":
            self.password = "Ab1234567890"
        else:
            self.password = "Nuomi20131127"
        keyworkClient = sms_v3_KeywordService()
        keyworkClient.setUsername(newAccount[0])
        keyworkClient.setPassword(self.password)
        keyworkClient.setToken("796fbec57ff499a2894ea4ac0b579c1b")
        #keyworkClient.setTarget(newAccount[0])

        adGroupClient = sms_v3_AdgroupService()
        adGroupClient.setUsername(newAccount[0])
        adGroupClient.setPassword(self.password)
        adGroupClient.setToken("796fbec57ff499a2894ea4ac0b579c1b")
        #adGroupClient.setTarget(accountInfo[0])

        indexNum = 0
        repeategroupNum = 0
        usefulgroupNum = 0
        for keywordinfo in self.keywordshow:
            if(cmp(keywordinfo, '') == 0):
                continue
            textList = keywordinfo.split('\t')
            if self.groupIdDict.has_key(textList[5]):
                repeategroupNum += 1
                continue
            else:
                self.groupIdDict[textList[5]] = 0
            #检查推广单元的状态
            adGroupIds = {"adgroupIds":[textList[5]]}
            adgroupInfo = adGroupClient.getAdgroupByAdgroupId(adGroupIds)

            tempInt = 0
            if adgroupInfo is not None and adgroupInfo['header'] is not None and adgroupInfo['header']['status'] != 0:
                print "response:"
                print adgroupInfo
                continue

            while(adgroupInfo is None or adgroupInfo['body'] is None or adgroupInfo['body']['adgroupTypes'] is None or (len(adgroupInfo['body']['adgroupTypes']) == 0) ):
                time.sleep(0.1)
                adgroupInfo = adGroupClient.getAdgroupByAdgroupId(adGroupIds)
                print adgroupInfo
                if(tempInt >2):
                    break
                tempInt += 1
            if(tempInt > 2):
                usefulgroupNum += 1
                continue
            if adgroupInfo['body']['adgroupTypes'][0]['status'] != 31:
                usefulgroupNum += 1
                continue

            keywordReq = {"keywordIds":[textList[7]]}
            time.sleep(0.05)
            resKeyWordInfo = keyworkClient.getKeywordByKeywordId(keywordReq)
            checkNum = 0
            while( resKeyWordInfo is None or resKeyWordInfo['body'] is None or resKeyWordInfo['body']['keywordTypes'] is None or len(resKeyWordInfo['body']['keywordTypes']) == 0):
                if(checkNum > 3):
                    break
                time.sleep(0.1)
                resKeyWordInfo = keyworkClient.getKeywordByKeywordId(keywordReq)
                checkNum += 1
            if(checkNum > 3):
                continue
            keywords = resKeyWordInfo['body']['keywordTypes']

            for keyword in keywords:
                print keyword
                indexNum += 1
                print 'repeatekeywords', repeategroupNum, 'adgroup unuseful', usefulgroupNum,'urlindex:', indexNum
                try:
                    strUrlPc = keyword['pcDestinationUrl']
                except Exception, e:
                    continue

                strUrl = strUrlPc
                if( strUrl != None and cmp(strUrl, "") != 0):
                    self.pcurlNum += 1
                    resTemp = ''
                    resTemp += newAccount[0] + '\t'
                    resTemp += textList[3] + '\t'
                    resTemp += textList[4] + '\t'
                    resTemp += textList[6] + '\t'
                    resTemp += keyword['keyword'].encode('utf-8') +'\t'
                    resTemp += 'pc' + '\t'
                    resTemp += keyword['pcDestinationUrl'].encode('utf-8')
                   # self.urlList.append(resTemp)
                try:
                    strUrlMobile = keyword['mobileDestinationUrl']
                except Exception, e:
                    continue

                strUrl = strUrlMobile
                if(strUrl != None and cmp(strUrl, "") != 0):
                    self.mobileurlNum += 1
                    resTemp = ''
                    resTemp += newAccount[0] + '\t'
                    resTemp += textList[3] + '\t'
                    resTemp += textList[4] + '\t'
                    resTemp += textList[6] + '\t'
                    resTemp += keyword['keyword'].encode('utf-8') + '\t'
                    resTemp += 'mobile' + '\t'
                    resTemp += keyword['mobileDestinationUrl'].encode('utf-8')
                    # self.urlList.append(resTemp)
                if(cmp(strUrlPc, "") == 0 and cmp(strUrlMobile, "") == 0):
                    resTemp = ''
                    resTemp += newAccount[0] + '\t'
                    resTemp += textList[3] + '\t'
                    resTemp += textList[4] + '\t'
                    resTemp += textList[6] + '\t'
                    resTemp += keyword['keyword'].encode('utf-8') + '\t'
                    resTemp += 'null' + '\t'
                    resTemp += "null"
                    # self.urlList.append(resTemp)
                self.FuncCheckUrl(resTemp)




    def FuncCheckUrl(self,line):
            print "readurl", self.readurlNum
            self.readurlNum += 1
            line = line.strip()
            textLine = line.split('\t')
            self.totalurlNum += 1
            resCheck = self.CheckUrl(textLine[0], textLine[6], textLine[5])
            if(cmp(resCheck, "") != 0):
                print resCheck
                self.errorurlNum += 1
                resTemp = list()
                resTemp.append(textLine[0])
                resTemp.append(textLine[1])
                resTemp.append(textLine[2])
                resTemp.append(textLine[3])
                resTemp.append(textLine[4])
                resTemp.append(resCheck)
                resTemp.append(textLine[5])
                resTemp.append(textLine[6])
                self.resList.append(resTemp)

    def CheckUrl(self, accountUser, strUrl, urlFlag):#urlFlag: pc, mobile
        strRes = ""
        header = {'Accept-Charset':'GBK,utf-8;q=0.7,*;q=0.3','User-Agent' : 'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)'}
        if(cmp(urlFlag, 'null') == 0):
            strRes += "空URL"
            self.nullUrlNum += 1
            return strRes
        try:
            if(cmp(urlFlag, 'pc') == 0):

                posSearch = strUrl.find('search')
                posDeal = strUrl.find('/deal/')
                vNuomiUrl = strUrl.find('v.nuomi.com')
                if(posDeal != -1):#deal table

                    """
                    1: filter repeat tinyurl, Distinguish pc and mobile
                    2: filter dead deal
                    """
                    posHtml = strUrl.find('.html?')
                    if((posHtml != -1) and (posHtml > posDeal)):#deal info
                        self.pcdealinfoNum += 1
                        posi = posDeal + 6
                        tiny_url = strUrl[posi: posHtml]

                        if(self.CheckRepeatUrl(tiny_url, urlFlag) == 0):# repeate url
                            self.pcrepeatetinyurlNum += 1
                            pass
                        elif self.deadDeal.has_key(tiny_url):
                            self.deadDealNum += 1
                            if self.CheckDeadDeal(self.deadDeal[tiny_url]):
                                strRes += "合理过期团单(" + self.deadDeal[tiny_url] + ")、"
                            else:
                                strRes += "非合理过期团单(" + self.deadDeal[tiny_url] + ")、"
                        else:
                            request = urllib2.Request(strUrl, headers = header)
                            urlHandle = urllib2.urlopen(request, timeout=self.openurltimeout)
                            html = urlHandle.read()
                            soup = BeautifulSoup(html)
                            soup1 = soup.find('body')
                            if soup1 is not None:
                                resTag = soup1.find('div', attrs={'class':'error-page error-404'})
                                if resTag is not None:
                                    strRes += "打开失败、"
                                    self.openurlErrorNum += 1

                            urlHandle.close()
                            time.sleep(0.05)
                    else:#筛选页:主要是 movie
                        self.pcdeallistNum += 1
                        request = urllib2.Request(strUrl, headers = header)
                        urlHandle = urllib2.urlopen(request, timeout=self.openurltimeout)
                        html = urlHandle.read()
                        soup = BeautifulSoup(html)
                        soup1 = soup.find('body')
                        soup2 = soup1.find('div', attrs={'class' : "w-large-list"})
                        if soup2 is not None:
                            classinfo = soup2.find('span')
                            if(classinfo.txt == "0" ):
                                strRes += "筛选无结果、"
                                self.noListResultNum += 1
                        urlHandle.close()
                        time.sleep(0.05)

                elif(posSearch != -1) :
                    self.searchurlNum += 1
                    request = urllib2.Request(strUrl, headers = header)
                    urlHandle = urllib2.urlopen(request, timeout=self.openurltimeout)
                    html = urlHandle.read()
                    soup = BeautifulSoup(html)
                    soup1 = soup.find('body')
                    soup2 = soup1.find('div', attrs={'class' : "page-body page-body-no-result"})
                    tempsoup2=soup1.find('div', attrs={'class' : "page-body"})
                    if(soup2 is None):
                        soup2=tempsoup2
                    if(soup2 is None):
                        strRes += "下载页面失败、"
                        self.openurlErrorNum += 1
                        urlHandle.close()

                    else:
                        classinfo = soup2.find('p', attrs={'class' : "noresult-tip"})
                        if(classinfo != None):#have searchTip searchTipNo, so have not deal
                            strRes += "搜索结果页无团单、"
                            self.noListResultNum += 1
                            urlHandle.close()
                    time.sleep(0.05)
                elif(vNuomiUrl != -1):
                    request = urllib2.Request(strUrl, headers = header)
                    urlHandle = urllib2.urlopen(request, timeout=self.openurltimeout)
                    html = urlHandle.read()
                    soup = BeautifulSoup(html)
                    soup1 = soup.find('body')
                    soup2 = soup1.find('div', attrs={'class' : "page-body"})
                    if(soup2 is None):
                        strRes += "筛选无结果、"
                        self.noListResultNum += 1
                        urlHandle.close()
                    else:
                        classinfo = soup2.find('p', attrs={'class' : "noresult-tip"})
                        if(classinfo != None):#have searchTip searchTipNo, so have not deal
                            strRes += "筛选无结果、"
                            self.noListResultNum += 1
                        urlHandle.close()
                    time.sleep(0.05)
                else :
                    posCategory = strUrl.find('category')
                    if(posCategory != -1):
                        self.pcothercatgoryurlNum += 1
                        request = urllib2.Request(strUrl, headers = header)
                        urlHandle = urllib2.urlopen(request, timeout=self.openurltimeout)
                        html = urlHandle.read()
                        soup = BeautifulSoup(html)
                        soup1 = soup.find('body')
                        if soup1 is not None:
                            soup2 = soup1.find('div', attrs={'class' : "homebg"})
                            if soup2 is not None:
                                classinfo = soup2.find('div', attrs={'class' : "upProduct clearfix"})
                                if(classinfo == None ):
                                    strRes += "筛选无结果、"
                                    self.noListResultNum += 1
                        urlHandle.close()
                        time.sleep(0.05)
                    else:
                        self.otherurlsampleNum += 1
                        #add sampling Strategy
                        if(self.sampleValue % self.sampleSeed == 0):
                            request = urllib2.Request(strUrl, headers = header)
                            urlHandle = urllib2.urlopen(request, timeout=self.openurltimeout)
                            html = urlHandle.read()
                            soup = BeautifulSoup(html)
                            soup1 = soup.find('body')
                            if soup1 is not None:
                                resTag = soup1.find('div',attrs={'class':'error-page error-404'})
                                if resTag is not None:
                                    strRes += "打开失败、"
                                    self.openurlErrorNum += 1
                            urlHandle.close()
                            time.sleep(0.05)
                        self.sampleValue += 1

            elif(cmp(urlFlag, 'mobile') == 0):
                posDeal = strUrl.find('/deal/view?tinyurl=')
                posTuanList = strUrl.find('/webapp/tuan/list?')
                if(posDeal != -1):
                    self.mobiledealinfoNum += 1
                    posDeal += 19
                    posj = strUrl.find('&', posDeal)
                    tiny_url = strUrl[posDeal:posj]
                    if(self.CheckRepeatUrl(tiny_url, urlFlag) == 0):#repeate url

                        self.mobilerepeatetinyurlNum += 1
                        pass
                    elif self.deadDeal.has_key(tiny_url):#dead url
                        self.deadDealNum += 1
                        if self.CheckDeadDeal(self.deadDeal[tiny_url]):
                            strRes += "合理过期团单(" + self.deadDeal[tiny_url] + ")、"
                        else:
                            strRes += "非合理过期团单(" + self.deadDeal[tiny_url] + ")、"

                    else:
                        if(self.sampleValueMobile % self.sampleSeedMobile == 0):
                            request = urllib2.Request(strUrl, headers = header)
                            urlHandle = urllib2.urlopen(request, timeout=self.openurltimeout)
                            urlHandle.close()
                            time.sleep(0.05)
                        self.sampleValueMobile += 1
                elif(posTuanList != -1):
                    request = urllib2.Request(strUrl, headers = header)
                    urlHandle = urllib2.urlopen(request, timeout=self.openurltimeout)
                    html = urlHandle.read()
                    soup = BeautifulSoup(html)
                    soup1 = soup.find('body')
                    if soup1 is not None:
                        soup2 = soup1.find('article', attrs={'class' : "p-list"})
                        if soup2 is not None:
                            classinfo = soup2.find('section', attrs={'class' : "no-result"})
                            if(classinfo != None):
                                self.noListResultNum += 1
                                strRes += "list无结果、"
                            urlHandle.close()
                            time.sleep(0.05)
                else:
                    self.otherurlsampleNum += 1
                    if(self.sampleValue % self.sampleSeed == 0):
                        request = urllib2.Request(strUrl, headers = header)
                        urlHandle = urllib2.urlopen(request, timeout=self.openurltimeout)
                        html = urlHandle.read()
                        soup = BeautifulSoup(html)
                        soup1 = soup.find('body')
                        if soup1 is not None:
                            resTag = soup1.find('div', attrs={'class':'p-error'})
                            if resTag is not None:
                                strRes += "打开失败、"
                                self.openurlErrorNum += 1

                        urlHandle.close()
                        time.sleep(0.05)
                    self.sampleValue += 1

        except HTTPError, e:
            traceback.print_exc()
            self.openurlErrorNum += 1
            strRes += 'http error、'
        except URLError, e:
            traceback.print_exc()
            self.openurlErrorNum += 1
            strRes += 'failed to reach server:、'
        except Exception, e:
            self.openurlErrorNum += 1
            strRes += e[0] + '、'
            traceback.print_exc()

        errorFlag = 0
        poscid = strUrl.find('cid=')
        poschannel = strUrl.find('channel=')
        if(( poscid != -1) or (poschannel != -1)):
            if(poscid == -1):
                pos = poschannel + 8
            else :
                pos = poscid + 4
                posj = strUrl.find('&', pos)
                cidNum = strUrl[pos : posj]
            if self.accountCid.has_key(accountUser):
                cidInfo = self.accountCid[accountUser]
                if(cidInfo.find(cidNum) == -1):
                    strRes += "非天兔cid:" + cidNum + "、"
                    self.errorCidNum += 1
        else :
            errorFlag = 1
            strRes += '链接无cid/channel、'

        if(strUrl.find('channel_content={keywordid}') == -1):
            errorFlag = 1
            strRes += '无channel_content、'

        if(strUrl.count('?') != 1):
            errorFlag = 1
            strRes += "0或多个?、"
        if(strUrl.find('?') > strUrl.find('&')):
            errorFlag = 1
            strRes += "?在&后面、"
        if(strUrl.find('&&') != -1):
            errorFlag = 1
            strRes += "连续出现两个&。"
        if(errorFlag == 1):
            self.formatErrorNum += 1
        return strRes

    def LoadAccountCid(self, filePath):
        inFileHandle = open(filePath, 'r')
        line = inFileHandle.readline()
        while line:
            line = line.strip()
            textLine = line.split(' ')
            self.accountCid.setdefault(textLine[0], textLine[1])
            line = inFileHandle.readline()
        inFileHandle.close();

    def LoadDeadDeal(self, filePath):
        inFileHandle = open(filePath, 'r')
        line = inFileHandle.readline()
        while line:
            line = line.strip()
            lineList = line.split('\t')
            self.deadDeal.setdefault(lineList[0], lineList[1])
            line = inFileHandle.readline()
        inFileHandle.close();

if __name__ == "__main__":
    if (len(sys.argv) != 2):
        print "please input index"
        sys.exit()
    reload(sys)
    sys.setdefaultencoding('utf8')
    try:
        now_time = datetime.datetime.now()
        print now_time.strftime('%Y-%m-%d %H:%M:%S')
        now_time = now_time + datetime.timedelta(days=-1)
        dateStr = now_time.strftime('%Y-%m-%d')
        index=int(sys.argv[1])
        print u'here'
        monitorHandle = CUrlMonitor(index)
        monitorHandle.start()
        print u'monitor'
        time.sleep(20)
        checkHandle = CUrlCheck(index, monitorHandle.accountInfo[index][0], dateStr)
        checkHandle.start()
        print u'check'
        now_time = datetime.datetime.now()
        print now_time.strftime('%Y-%m-%d %H:%M:%S')
    except Exception, e:
        print e
        tb.print_exc()



