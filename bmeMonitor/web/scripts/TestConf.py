#! /usr/bin/env python
# -*- coding:UTF-8 -*-
   
# Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved
# 2014-10-30 19:22:28 chengyunlai
 
'''
@file src.TestConf.py
@author chengyunlai (chengyunlai@baidu.com)
@date 2014-10-30 19:22:28
@brief 
'''

TEST_URL_LIST = []
TEST_SERVER = {}


def __init__():
    global TEST_URL_LIST
    global TEST_SERVER
    
    TEST_SERVER['host'] = "tsm.nuomi.com"
    TEST_SERVER['port'] = 80
    
    # BES渠道
    TEST_URL_LIST.append({
        'name':'BES',
        'url':('/ClickService/click?url=http%3A%2F%2Fclick%2Ebes%2Ebaidu%2Ecom%2Fadx%2Ephp%3Fc%3Dcz1hMTc1MTE3YzU2OGU'
               '3YTg1AHQ9MTQxMzk4MDE1NgBzZT0xAGJ1PTczOTQ3NTgAdHU9OTIyMzM3MjAzMjU2MTQ2ODY4NwBhZD0yMzI0Mzg1NjMAc2l0ZT1'
               'odHRwOi8vd3d3LjNqeS5jb20vamluZ2h1YS8yNi8yMzMwMjZfMjEuaHRtbAB2PTEAaT0yYzc5OWQ3ZA%26k%3Ddz00NjgAaD02MA'
               'Bjc2lkPTI1NzY5ODAzODIyOAB0bT0xMzE0MTAyAHRkPTE2NjAxNzUAZm49bGlkYWZhbmdzaGVuZ19jcHIAZmFuPQB1aWQ9NzM5NT'
               'A0MgBjaD0wAG9zPTEwAGJyPTEyAGlwPTE4Mi44NS4xOTAuMjIAc3NwPTEAYXBwX2lkPQB0dHA9MQBjb21wbGU9MABzdHlwZT0w%2'
               '6url%3Dhttp%253A%252F%252Fwww.nuomi.com%253Fcid%253Dtsmdsp_bes%2526channel_content%253Def5b8420621e3'
               '5264b23d05c0a50ed87'),
        'location':'http://www.nuomi.com/?cid=tsmdsp_bes&channel_content=ef5b8420621e35264b23d05c0a50ed87',
    })
    # 晶赞渠道
    TEST_URL_LIST.append({
        'name':'zamplus',
        'url':('/ClickService/click?channel_content=239ry882131294hgq94&cid=tsm_dsp_zamplus&url=http%3A%2F%2Fla.nuom'
               'i.com%2Fdeal%2Fsgmsfuso.html%3Fcid%3Dtsm_dsp_zamplus'),
        'location':'http://la.nuomi.com/deal/sgmsfuso.html?cid=tsm_dsp_zamplus&channel_content=239ry882131294hgq94',
    })
    # 1- 360渠道
    TEST_URL_LIST.append({
        'name':'360',
        # 'url':('/ClickService/click?sign=4626d9bc9496371b7fd7ea7265d257c3&active_time=1398326393&from_url=http://tua'
        #       'n.360.cn/shi_jia_zhuang/c_301.html?tds=1&area=91&pageno=1&qname=ghz321&qihoo_id=36040&qid=282700288&'
        #       'qmail=&bid=2000287&url=http%3a%2f%2fsjz.nuomi.com%2fdeal%2fc3lndta8.html%3futm_source%3d360%26utm_me'
        #       'dium%3dneiye-pic%26utm_campaign%3ddaohang%26cid%3d000302%26ext%3d1afg9q02phwvb03d7ddd'),
        'url':('/ClickService/click?sign=4626d9bc9496371b7fd7ea7265d257c3&active_time=1398326393&from_url=http://tuan'
               '.360.cn/shi_jia_zhuang/c_301.html?tds=1&area=91&pageno=1&qname=ghz321&qihoo_id=36040&qid=282700288&qm'
               'ail=&bid=2000287&url=http%3a%2f%2fsjz.nuomi.com%2fdeal%2fc3lndta8.html%3futm_source%3d360%26utm_mediu'
               'm%3dneiye-pic%26utm_campaign%3ddaohang%26cid%3d000302%26ext%3d1afg9q02phwvb03d7ddd'),
        # 'location':'http://sjz.nuomi.com/deal/rqao1jim.html?utm_source=360&utm_medium=neiye-pic&utm_campaign=daohang&cid=000302',
        'location':'http://www.nuomi.com/deal/kiuv02wk.html?utm_source=360&utm_medium=neiye-pic&utm_campaign=daohang&cid=000302',
        'cps_id':8,
        'cps_info':'{"qihoo_id":"36040","qid":"","cps_id":8,"ext":"1e2orr02z8o2z0h23287"}',
        
    })
    # 2- 金山团购
    TEST_URL_LIST.append({
        'name':'duba',
        'url':('/ClickService/click?cid=007401&sessionkey=LzF1LzIuMTRjW2AtMGUtNCkwX19jXDQtZC8xYTM1W2QyLWU%3D&tn=f3bb'
                'c2be9fbb248543378a0837391554&ijinshantmp=42&ijinshan_uid=cd57522657c8bd43035b413d6cca14c7&url=http%'
                '3a%2f%2fbj.nuomi.com%2fdeal%2fdzsqcc0z.html%3fcid%3d007401'),
        'location':'http://bj.nuomi.com/deal/dzsqcc0z.html?cid=007401',
        'cps_id':10,
        'cps_info':('{"ijinshan_uid":"cd57522657c8bd43035b413d6cca14c7","tn":"f3bbc2be9fbb248543378a0837391554","ses'
                    'sionkey":"LzF1LzIuMTRjW2AtMGUtNCkwX19jXDQtZC8xYTM1W2QyLWU=","cps_id":10,"ijinshantmp":"42"}'),
    })
    # 3- 团800链接 cid=0 主站   cid=1 联盟 cid=2 wap
    TEST_URL_LIST.append({
        'name':'tuan800-pc',
        # 'url':('/ClickService/click?cid=0&outsrc=tuan800&src=tuan800&uid=02322&url=http%3A%2F%2Fsh.nuomi.com%2Fdeal%2F'
        #       'jzx7fsu5.html%3Futm_source%3Dtuan800%26utm_medium%3Dpic%26utm_campaign%3Ddaohang%26cid%3D000702&wi=544'
        #       '8ed8bfbdde46ebb000a2f'),
        'url':('/ClickService/click?cid=0&outsrc=tuan800&src=tuan800&uid=02455&url=http%3A%2F%2Fbj.nuomi.com%2Fdeal%2F'
               'kx3spcem.html%3Futm_source%3Dtuan800%26utm_medium%3Dpic%26utm_campaign%3Ddaohang%26cid%3D000702&wi=545'
               '284627d866e26b600160f'),
        # 'location':'http://sh.nuomi.com/deal/jzx7fsu5.html?utm_source=tuan800&utm_medium=pic&utm_campaign=daohang&cid=000702',
        'location':'http://bj.nuomi.com/deal/kx3spcem.html?utm_source=tuan800&utm_medium=pic&utm_campaign=daohang&cid=000702',
        'cps_id':6,
        'cps_info':'{"uid":"02836","wi":"545283a0fbdde4922b0015c6","cps_id":6,"src":"tuan800","cid":"0"}',
    })
    
    # 3- 团800链接 cid=0 主站   cid=1 联盟 cid=2 wap
    TEST_URL_LIST.append({
        'name':'tuan800-wap',
        'url':('/ClickService/click?cid=2&outsrc=tuan800&src=tuan800&uid=02557&url=http%3A%2F%2Fm.nuom'
               'i.com%2Fdeal%2Fview%3Ftinyurl%3Diygezk6f%26utm_source%3Dtuan800%26utm_medium%3Dpic%26utm_campaign%3Dda'
               'ohang%26cid%3D000702&wi=545287607d866e26b60016fe'),
        'location':'http://m.nuomi.com/deal/view?tinyurl=iygezk6f&utm_source=tuan800&utm_medium=pic&utm_campaign=daohang&cid=000702',
        'cps_id':6,
        'cps_info':'{"uid":"02869","wi":"5452881f27c6eeab5100019e","cps_id":6,"src":"tuan800","cid":"2"}',
    })
    
    # 4- 领克特
    TEST_URL_LIST.append({
        'name':'linkt',
        'url':('/ClickService/click?utm_source=linkt&utm_medium=cps&cid=001703&a_id=11&c_id=11&l_id=11&l_type1=11&url='
               'http%3A%2F%2Fwww.nuomi.com%2Fdeal%2Fcspxiaua.html'),
        'location':'http://www.nuomi.com/deal/cspxiaua.html?utm_medium=cps&utm_source=linkt&cid=001703',
        'cps_id':5,
        'cps_info':'{"a_id":"11","l_type1":"11","cps_id":5,"c_id":"11","l_id":"11"}',
    })
    # 5- 多麦网盟   to改成url
    TEST_URL_LIST.append({
        'name':'duomai',
        'url':('/ClickService/click?feedback=60619_399_127971__1&url=http%3A%2F%2Fwww.nuomi.com%2F%3Ffeedbac'
               'k%3D60619_399_127971__1%26utm_source%3Ddm%26utm_medium%3Dcps%26utm_campaign%3Dunion%26cid%3'
               'D007501'),
        'location':'http://www.nuomi.com/?feedback=60619_399_127971__1&utm_source=dm&utm_medium=cps&utm_campaign=union&cid=007501',
        'cps_id':11,
        'cps_info':'{"feedback":"60619_399_127971__1","cps_id":11,"mid":""}',
    })
    # 6- 51返利 target_url改为url
    TEST_URL_LIST.append({
        'name':'51fanli',
        'url':('/ClickService/click?tracking_id=1457779384&channel_id=51fanli&u_id=17&url=http%3A%2F%'
               '2Fwww.nuomi.com%3Futm_source%3D51fanli%26utm_medium%3Ddenglu%26utm_campaign%3Dpic%26cid%3D00'
               '1701%2F%3F&tracking_code=211023&code=&syncname=false&username=&usersafekey=&action_time=&ema'
               'il=&show_name=&syncaddress=&name=&province=&city=&area=&address=&zip=&phone=&mobile='),
        'location':('http://www.nuomi.com/?utm_source=51fanli&utm_medium=denglu&utm_campaign=pic&cid=001701/?'
                    '&tracking_code=211023&u_id=17&username=&utm_source=51fanli&utm_medium=denglu&utm_campaig'
                    'n=pic&cid=001701'),
        'cps_id':2,
        'cps_info':'{"tracking_code":"211023","username":"","cps_id":2,"u_id":"17"}',
    })
    # 7- 51比购
    TEST_URL_LIST.append({
        'name':'51bigou',
        'url':'/ClickService/click?utm_source=51bi&utm_medium=cps&cid=001702&u_id=216321937&url=http%3A%2F%2Fwww.nuomi.com',
        'location':'http://www.nuomi.com/?utm_medium=cps&utm_source=51bi&cid=001702',
        'cps_id':14,
        'cps_info':'{"cps_id":14,"u_id":"218769031"}',
    })
    # 8- 亿起发
    TEST_URL_LIST.append({
        'name':'yiqifa',
        'url':'/ClickService/click?src=emar&channel=cps&cid=002201&wi=NDgwMDB8dGVzdA&url=http://www.nuomi.com/',
        'location':'http://www.nuomi.com/?wi=NDgwMDB8dGVzdA&cid=002201',
        'cps_id':3,
        'cps_info':'{"wi":"NDgwMDB8dGVzdA","cps_id":3}',
    })
    
    # 9- 百度团购
    TEST_URL_LIST.append({
        'name':'百度团购',
        'url':('/ClickService/click?url=http%3A%2F%2Fbj.nuomi.com%2Fdeal%2Fbbtj9ovk.html%3Futm_source%3Dbaidu'
               '-cps%26amp%3Butm_medium%3Dny-pic%26amp%3Butm_campaign%3Dny-pic%26amp%3Bcid%3D006001%26tn%3Dba'
               'idutuan_tg%26baiduid%3D350020c3ce54a3dfeaed01564acfe69f&salt=ac5e5a35f4bfd0c080d1801ccc5f490e'),
        'location':('http://bj.nuomi.com/deal/bbtj9ovk.html?utm_source=baidu-cps&utm_medium=ny-pic&utm_campai'
                    'gn=ny-pic&cid=006001&tn=baidutuan_tg&baiduid=350020c3ce54a3dfeaed01564acfe69f'),
        'cps_id':1,
        'cps_info':'{"tn":"baidutuan_tg","baiduid":"350020c3ce54a3dfeaed01564acfe69f"}',
    })
    
    '''
    # 9- 51返利联合登陆
    TEST_URL_LIST.append({
        'name':'login',
        'url':('/ClickService/click?click_type=login&tracking_id=123123&channel_id=51fanli&u_id=6&target_url=&tracking_cod'
               'e=12345&code=d7b6e7b74aea236623ea1aa6830f6360&syncname=true&username=12345@51fanli&usersafekey=849b59ee2e3'
               'af476&action_time=1294820691&email=6@51fanli.com&show_name=qiubo%40%B7%B5%C0%FB%CD%F8&syncaddress=true&nam'
               'e=%D0%EC%B2%A8&province=%C9%CF%BA%A3%CA%D0&city=%C9%CF%BA%A3%CA%D0&area=%C6%D6%B6%AB%D0%C2%C7%F8&address=%'
               'D5%C5%D1%EE%C2%B7707&zip=200000&phone=021-58888400&mobile=15888888888'),
        'location':''
    })
    '''
    pass

__init__()


