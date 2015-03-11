# !/usr/bin/env python
# -*- coding: UTF-8 -*-

################################################################################
#
# Copyright (c) 2015 Baidu.com, Inc. All Rights Reserved
#
#################################################################################
"""
Wise阿拉丁页面监控 配置

Authors: chengyunlai@baidu.com
Date:    2015/03/08 23:55:06

"""

import copy
import httplib
import json
import thread
import threading
import time
import urllib
import logging

import bs4

from ApiWiseConf import *

class WiseAladdinParser(object):
    """阿拉丁卡片解析类
    """

    def __inif__(self):
        pass

    def parse(self, htmlpage):
        alaSoup = bs4.BeautifulSoup(htmlpage)
        alaCard = alaSoup.find("div",class_="result", srcid = WISE_SRC_NAME)
        if not alaCard:
            return None
        else: return alaCard
pass

class WiseClient(object):
    """Wise阿拉丁 请求客服端
    """

    REQ_DEFAULT_HEADER = {
        'Accept-Charset':'GBK,utf-8;q=0.7,*;q=0.3',
        "User-Agent": ("Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) "
                       "AppleWebKit/600.1.3 (KHTML, like Gecko) Version/8.0 "
                       "Mobile/12A4345d Safari/600.1.4"),
        "Cookie": "BAIDULOC=12958160.97_4825907.72_200_131_1413448032644"
    }

    REQ_RETRY = 5

    def __init__(self, svrHost = "m.baidu.com", svrPort = 443):
        """初始化,默认https连接

        Args:
            svrHost: Wise阿拉丁请求的服务器地址
            svhPort: Wise阿拉丁请求的服务端口

        """
        self._svrhost = svrHost
        self._svrport = svrPort
        self.req_conn = httplib.HTTPSConnection(self._svrhost, self._svrport)
        self.headers = copy.deepcopy(WiseClient.REQ_DEFAULT_HEADER)

    def __del__(self):
        self.req_conn.close()

    def __str__(self):
        return "[WiseClient] svrhost = {0}, svrport = {1}".format(self._svrhost, self._svrport)
    
    def _mergeCookie(self, _headers):
        pass


    def request(self, cityname, keyword):
        """请求Wise阿拉丁

        Args:
            cityname: 请求的定位城市名称,如 北京
            keyword: 请求的query，如 附近的团购

        Returns:
            二元组，(状态码, Html)
            如果http返回正常，则为http状态码;
            如果重试最大次数都无返回, 则返回 -1，None

        """
        if cityname not in WISE_REQ_COOKIE_BAIDULOC_MAP:
            logging.info("[WiseClient] %s is not in baiduloc map!" % cityname)
            return None

        req_path = '/s?' + urllib.urlencode({'word': keyword})
        self.headers['Cookie'] = WISE_REQ_COOKIE_BAIDULOC_MAP[cityname]
        
        alreadyTry = 0
        while alreadyTry < WiseClient.REQ_RETRY:
            try:
                alreadyTry += 1
                logging.info("[WiseClient] try %d, request http://%s:%d/%s" % \
                        (alreadyTry, self._svrhost, self._svrport, req_path))
                self.req_conn.request('GET', req_path, None, self.headers)
                resp = self.req_conn.getresponse()
                self._mergeCookie(resp.getheaders())

                resp_code = resp.status
                resp_html = resp.read()
                logging.info("[WiseClient] try %d, response status = %d" % (alreadyTry, resp_code))
                if resp_html and resp_code == 200:
                    return resp_code, resp_html

            except Exception as ex:
                logging.error(str(ex))
                time.sleep(3)            
        
        return -1, None
    


client = WiseClient()
rcode, rhtml = client.request("北京","附近的团购")

alaparser = WiseAladdinParser()
alaCard = alaparser.parse(rhtml)
print alaCard.prettify().encode("utf8")
print "-------------------------------"
rcode, rhtml = client.request("上海","附近的团购")
alaCard = alaparser.parse(rhtml)
print alaCard.prettify().encode("utf8")

exit()

"""    
class WiseRunner:
    
    def __init__(self, tasklist, ccdict, syscfg):
        self.stime = time.time()
        self.tasklist = tasklist
        self.currIdx = 0
        self.ccdict = ccdict
        self.lock = thread.allocate_lock()
        self.groups = int(syscfg.get('request', 'thread'))
        self.outfile = syscfg.get('request', 'result')
    
    def _update(self, td):
        '''Update thread list when hander finished .
        '''
        self.thlist.remove(td)
        if not self.thlist: self._afterProcess()

    def _afterProcess(self):
        cmd = 'cat {0}* | sort -n > {1}; rm {2}*; '.format(self.outfile + 'td', self.outfile, self.outfile + 'td')
        print cmd
        import os 
        os.system(cmd) 
        self.etime = time.time()
        print 'All done, time cost %f s' % (self.etime - self.stime)
        pass
        
    def start(self):
        tlen = len(self.tasklist)
        glen = tlen / self.groups + 1
        gs = 0
        ge = gs + glen
        self.thlist = []
        while ge <= tlen:
            aTh = self._asyncTask(gs, self.tasklist[gs:ge], self.outfile + 'td')
            aTh.set_controller(self)
            self.thlist.append(aTh)
            print 'TASK %d - %d : prepared ok ...' % (gs, ge)
            gs = ge
            ge = gs + glen
        if gs < tlen and ge > tlen:
            ge = tlen
            aTh = self._asyncTask(gs, self.tasklist[gs:ge], self.outfile + 'td')
            aTh.set_controller(self)
            self.thlist.append(aTh)
            print 'TASK %d - %d : prepared ok ...' % (gs, ge)
        
        print 'All prepared ok, start to send request ...'
        for t in self.thlist:
            t.start()        
        pass

    def _asyncTask(self, start_pos, task, outfile):
        return AsyncSender(self.ccdict, start_pos, task, outfile)
    
    pass


class AsyncSender(threading.Thread):
    def __init__(self, ccdict, start_pos, task, outfile):
        threading.Thread.__init__(self)
        self.task = task
        self.start_pos = start_pos
        self.ws = WiseTuanHander()
        self.ws.initCityCookies(ccdict)
        self.outfile = outfile + str(self.start_pos)
        pass
   
    def set_controller(self, ctl):
        self.ctl = ctl

    def run(self):
        fout = open(self.outfile, 'w')
        for que in self.task:
            self.ws.setQuery(que)
            self.ws.do_request()
            card = self.ws.extractRes()
            print >> fout, self.start_pos, '\t', json.dumps(card, ensure_ascii=False)
            self.start_pos += 1
            time.sleep(0.01)
        fout.close()
        print 'TASK %d - %d : DONE.' % (self.start_pos - len(self.task), self.start_pos)
        if self.ctl:
            self.ctl.lock.acquire()
            self.ctl._update(self)
            self.ctl.lock.release()

class WiseTuanHander:
    Feature_Word = 'wise_tuan'
    headers = {
        'Accept-Charset':'GBK,utf-8;q=0.7,*;q=0.3',
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.3 (KHTML, like Gecko) Version/8.0 Mobile/12A4345d Safari/600.1.4",
        "Cookie": "BAIDULOC=12958160.97_4825907.72_200_131_1413448032644"
    }
    WISE_HOST = 'tc-mbu-web13.epc.baidu.com'
    WISE_PORT = "8003"

    def __init__(self, query=['北京', '附件的团购']):
        self.query = query
    
    def initCityCookies(self, city_cookie_dict):
        if type(city_cookie_dict) == dict:
            self.city_cookie_dict = city_cookie_dict
        else:
            with open(city_cookie_dict, 'r') as fin:
                ccs = fin.readlines()
            self.city_cookie_dict = {}
            for cc in ccs:
                cc = cc.strip()
                if not cc: continue
                cc = eval(cc)
                print cc
                self.city_cookie_dict[cc[0]] = cc[1]
                # print cc
        return self.city_cookie_dict
    
    def do_request(self):
        conn = httplib.HTTPConnection(WiseTuanHander.WISE_HOST, WiseTuanHander.WISE_PORT)
        self.path = '/s?' + urllib.urlencode({'word':self.query[1]})
        # 根据城市信息返回 header
        if (self.city_cookie_dict.has_key(self.query[0])):
            header = copy.deepcopy(WiseTuanHander.headers)
            # print 'has_key'
            header['Cookie'] = self.city_cookie_dict[self.query[0]]
        else:
            header = WiseTuanHander.headers
            # print 'no_key'
        
        conn.request('GET', self.path, None, header)
        resp = conn.getresponse()
        self.responseHtml = resp.read()
        self.responseStatus = resp.status
        self.responseReason = resp.reason
        conn.close()
        # self._report_last()
    
    def _report_last(self):
        reptpl = "{0} http://{1}:{2}{3}"
        reptxt = reptpl.format(self.responseStatus,
            WiseTuanHander.WISE_HOST, WiseTuanHander.WISE_PORT, self.path)
        print reptxt
    
    def hasFeature(self):
        return self.responseHtml.find(WiseTuanHander.Feature_Word)
    
    def extractRes(self):
        ''' 
        提取wise_tuan卡片信息，
        @return: 数据结构为一个字典,详细字段如下：
            query :     请求关键词
            city ：     城市
            tpos :      出现wise_tuan标识的位置，如果没有召回 值为 -1，此时无后续字段
            rpos ：     召回卡片位置 ， 例如 1表示置顶
            title :     返回卡片标题
            deals :     为返回团单列表 ，数据结构为 List，包含每个返回团单的title+description
        '''
        card = {'query':self.query[1], 'city':self.query[0]} 
        text_pos = self.hasFeature()
        card['tpos'] = text_pos
        if text_pos <= 0 :return card 
        # 解析详细信息
        resList = bs4.BeautifulSoup(self.responseHtml).find_all('div', class_='result')
        result_pos = 0  # 计算卡片位置
        for res in resList:
            result_pos += 1
            if str(res).find(WiseTuanHander.Feature_Word) > 0:
                card['rpos'] = result_pos
                card['title'] = res.find('a', class_='wm-box-adaptive wm-title-lightapp').get_text().encode('utf8')
                card['deals'] = []
                for deal in res.find_all('a', class_="wm-box-flexboxContainer wa-wise-tuan-list"):
                    card['deals'].append(deal.get_text().encode('utf8'))
                break
        return card
    
    def respText(self):
        return self.responseHtml
    
    def respCode(self):
        return self.responseStatus
    
    def setQuery(self, query):
        self.query = query

pass
"""
