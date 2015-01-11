#!/usr/bin/env python
#-*- coding: utf-8 -*-

from subprocess import call
from logLib import *

def msgSend(phonenum_list, msg_content, mode="gsm"):
    if(mode == "gsm"):
        for phonenum in phonenum_list:
            cmd = "gsmsend -s emp01.baidu.com:15003 "+phonenum+"@"+"\""+msg_content+"\""
            #print cmd
            Ret=call(cmd, shell=True)
            if(Ret != 0):
                logging.error("msgSend failed!")
    elif(mode == "qapi"):
        for phone in phonenum_list:
            cmdstr = '''curl -i -X POST \
-H "X_Authorization:54f6babfea263797ea6b681da19b417d" \
-H "Accept:application/json" \
-d '{ \
 "number":"''' + phone + '''", \
 "content":"''' + msg_content + '''" \
}' \
'http://qapi.baidu.com/api/sms_service/sms_send/V0.1/sms'
            '''
            #print cmdstr
            Ret=call(cmdstr, shell=True)
            if(Ret != 0):
                logging.error("msgSend failed!")

if __name__ == '__main__':
    msgSend(['18665817689'], u'【告警】userPreference:getResponse failed 3 times.', mode="qapi")

