# !/usr/bin/env python
# -*- coding: UTF-8 -*-

################################################################################
#
# Copyright (c) 2015 Baidu.com, Inc. All Rights Reserved
#
#################################################################################
"""
短信通知辅助工具

Authors: yangjun03@baidu.com, chengyunlai@baidu.com
Date:    2015/03/06 20:55:06
"""

from subprocess import call
from logLib import *

def msgSend(phonenum_list, msg_content, mode="gsm"):
    """发送短信通知

    Args:
        phonenum_list: 短信接收手机列表
        msg_content: 短信内容，为UTF-8编码
        mode: 短信发送方式，支持 gsm 和 qapi两种

    """
    if(mode == "gsm"): # GSM方式要求发送内容为GBK编码
        for phonenum in phonenum_list:
            cmdStr = "gsmsend -s emp01.baidu.com:15003 {0}@\"{1}\"".format(phonenum, msg_content)
            cmdStr = cmdStr.decode("utf8").encode("gbk")
            ret = call(cmdStr, shell=True)
            if(ret != 0): logging.error("msgSend failed!")
    elif(mode == "qapi"):
        qapiCfg = {
            "H" : { "X_Authorization": "54f6babfea263797ea6b681da19b417d", "Accept": "application/json", },
            "d" : { "number": ",".join(phonenum_list), "content": msg_content, },            
        }
        header = " ".join([ "-H \"{0}:{1}\"".format(k, v) for k, v in qapiCfg["H"].items() ])
        data = "-d '{ " + ",".join([ '"{0}":"{1}"'.format(k, v) for k, v in qapiCfg['d'].items() ]) + " }'"
        messageContent = { "header" : header, "data" : data, "apiurl": "http://qapi.baidu.com/api/sms_service/sms_send/V0.1/sms", }
        cmdStr = """curl -i -X POST {header} {data} '{apiurl}'""".format(**messageContent)
        ret = call(cmdStr, shell = True)
        if ret != 0: logging.error("msgSend failed!")

# for test
if __name__ == '__main__':
    #msgSend(['18665817689','18810603945','18612987615'], '[告警] Send by qapi.', mode="qapi")
    #msgSend(['18665817689','18810603945','18612987615'], '[告警] Send by GSM.', mode="gsm")
    msgSend(['18810603945'], '[告警] Send by qapi.', mode="qapi")
    msgSend(['18810603945'], '[告警] Send by GSM.', mode="gsm")

