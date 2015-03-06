#coding=utf-8
import suds
import traceback as tb
from ApiSDKSoapClient import ApiSDKSoapClient
from ApiSDKSoapClient import printSoapResponse

from sms_v3_KeywordService import *

if __name__ == "__main__":
    try:
        service = sms_v3_KeywordService()
        request = {"keywordTypes":[{"keywordId":12345}]}
        newres = service.updateKeyword(request)
        printJsonResponse(newres)
        '''
        # init client stub
        apiSDKSoapClient = ApiSDKSoapClient('sms','v3','KeywordService')
        newClient = apiSDKSoapClient.newSoapClient()

        request = newClient.factory.create('updateKeywordRequest')
        keywordType = newClient.factory.create('updateKeywordRequest.keywordTypes')
        keywordType.keywordId=12345
        request.keywordTypes=[]
        request.keywordTypes.append(keywordType)
        
        
        newClient.service.updateKeyword(request.keywordTypes)
        
        res = newClient.last_received()
        printSoapResponse(res)
        '''
        
    except Exception, e:
        print e
        tb.print_exc()

