#coding=utf-8
import base64
import gzip
import StringIO
import suds
import traceback as tb
from ApiSDKSoapClient import ApiSDKSoapClient
from ApiSDKSoapClient import printSoapResponse
from sms_v3_RankService import *
from  PreviewUtil import *

if __name__ == "__main__":
    try:
        service = sms_v3_RankService()
        newres = service.getPreview({"keyWords":["鲜花","团购"],"device":0,"region":1000,"page":0,"display":0})
        printJsonResponse(newres)
        print PreviewUtil.decode(newres["body"]["previewInfos"][0]["data"])
        '''
        # init client stub
        apiSDKSoapClient = ApiSDKSoapClient('sms','v3','RankService')
        newClient = apiSDKSoapClient.newSoapClient()

        request = newClient.factory.create('getPreviewRequest')
        request.keyWords = []
        request.keyWords.append("鲜花")
        request.device = 0
        request.region = 1000
        request.page = 0
        request.display = 0
        newClient.service.getPreview(request.keyWords,request.device,request.region,request.page,request.display)

        
        res = newClient.last_received()
        

        cstr = StringIO.StringIO(base64.b64decode(res.getChild("Envelope").getChild("Body").getChild('getPreviewResponse').getChild('previewInfos').getChild('data').getText()))
        ziper = gzip.GzipFile(fileobj=cstr)
        data = ziper.read()
        print data
        
        printSoapResponse(res)
        '''
        
    except Exception, e:
        print e
        tb.print_exc()

