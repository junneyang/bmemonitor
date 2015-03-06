#coding=utf-8
import suds
import traceback as tb
from ApiSDKSoapClient import ApiSDKSoapClient
from ApiSDKSoapClient import printSoapResponse

from sms_v3_AccountService import *

if __name__ == "__main__":
    try:
        service = sms_v3_AccountService()
        newres = service.getAccountInfo()
        printJsonResponse(newres)
        
        '''
        # init client stub
        apiSDKSoapClient = ApiSDKSoapClient('sms','v3','AccountService')
        
        newClient = apiSDKSoapClient.newSoapClient()

		#==== get account info ====
        newClient.service.getAccountInfo()

        # receive response and print result
        res = newClient.last_received()
        printSoapResponse(res)
        '''
        
#        request = newClient.factory.create('updateAccountInfoRequest')
#        accountInfoType = newClient.factory.create('updateAccountInfoRequest.accountInfoType')
#        excludeIp  = ['192.168.2.3','10.10.10.16','1.1.1.1.1.1']
#        accountInfoType.excludeIp  = excludeIp
#        request.accountInfoType=accountInfoType
#        
#        newClient.service.updateAccountInfo(request.accountInfoType)
#        
#        res = newClient.last_received()
#        printSoapResponse(res)


    except Exception, e:
        print e
        tb.print_exc()

