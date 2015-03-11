#coding=utf-8
import json  
import requests
from AuthHeader import *
from JsonEnvelop import *
import ConfigParser
import traceback as tb

'''
    json client
'''
class ApiSDKJsonClient():
    #client params
    __productline=None
    __version=None
    __service=None
    __url=None
    __username=None
    __password=None
    __token=None
    __target=None
    __accessToken=None
    __action=None

    #conf params
    urlconf=None
    usernameconf=None
    passwordconf=None
    tokenconf=None
    targetconf=None
    actionconf=None
    
    def __init__(self, productline,version,service): 
        try:
            self.initConfig()
            self.__productline=productline
            self.__version=version
            self.__service=service
            self.__url=self.urlconf
            self.__username=ApiSDKJsonClient.usernameconf
            self.__password=ApiSDKJsonClient.passwordconf
            self.__token=ApiSDKJsonClient.tokenconf
            self.__target=ApiSDKJsonClient.targetconf
            self.__action=ApiSDKJsonClient.actionconf
        except Exception, e:
            print e
            tb.print_exc()
            
    def initConfig(self):
        if (ApiSDKJsonClient.actionconf==None):
            cf = ConfigParser.ConfigParser()
            cf.read("baidu-api.properties")
            ApiSDKJsonClient.urlconf=cf.get("api", "serverUrl")
            ApiSDKJsonClient.usernameconf=unicode(cf.get("api", "username"),"utf-8")
            ApiSDKJsonClient.passwordconf=cf.get("api", "password")
            ApiSDKJsonClient.tokenconf=cf.get("api", "token")
            ApiSDKJsonClient.targetconf=cf.get("api", "target")
            ApiSDKJsonClient.actionconf=cf.get("api", "action")
            
    def execute(self,method,request):
        try:
            url = self.__url + '/json/'+self.__productline+'/'+self.__version+'/' + self.__service + '/' +method
            header = AuthHeader(username=self.__username,password=self.__password,token=self.__token,target=self.__target,accessToken=self.__accessToken)
            if (request is None):
                request = {}
            jsonEnv = JsonEnvelop(header,request)
            jsonStr=json.dumps(jsonEnv, default=convert_to_builtin_type, skipkeys=True)
            print jsonStr
            headers = {'content-type': 'application/json;charset=utf-8'}
            r = requests.post(url,data=jsonStr,headers=headers)
            return r.json()
        except Exception, e:
            print e
            tb.print_exc()
            
    def setUrl(self,url):
        self.__url=url
    def setUsername(self,username):
        self.__username=username
    def setPassword(self,password):
        self.__password=password
    def setToken(self,token):
        self.__token=token
    def setTarget(self,target):
        self.__target=target
    def setAccessToken(self,accessToken):
        self.__accessToken=accessToken

'''
    print response result
'''
def printJsonResponse(res):
        resheader = res["header"]
        resbody = res["body"]
        failures = resheader["failures"]
        print "Response Header=>"
        print "Execution result: \t", resheader["desc"]
        print "      operations: \t", resheader["oprs"]
        print "  operation time: \t", resheader["oprtime"]
        if (resheader["quota"] is not None):
            print "   consume quota: \t", resheader["quota"]
            
        if (resheader["rquota"] is not None):
            print "    remain quota: \t", resheader["rquota"]
            
        print "          status: \t", resheader["status"]
        if failures is not None:
            for failure in failures:
                print "            code: \t", failure["code"]
                print "         message: \t", failure["message"]
                print "        position: \t", failure["position"]
                
        print "Response Body=>"
        if resbody is not None:
            jsonStr=json.dumps(resbody, default=convert_to_builtin_type, skipkeys=True)
            print jsonStr





#转换函数
def convert_to_builtin_type(obj):
    # 把MyObj对象转换成dict类型的对象
    d = {}
    d.update(obj.__dict__)
    return d


#header = AuthHeader("rongdajun1","Aa456123","1085ffb557845b3d75d75b7762c8910a")
#jsonEnv = JsonEnvelop(header)
#jsonEnv.setBody({"keyWords":["购物"],"device":0,"region":1000,"page":0,"display":0})
#jsonStr=json.dumps(jsonEnv, default=convert_to_builtin_type, skipkeys=True)
#print jsonStr
##print myobj_instance
#
#headers = {'content-type': 'application/json;charset=utf-8"'}
#r = requests.post('https://api.baidu.com/json/sms/v3/RankService/getPreview',data=jsonStr,headers=headers)
#print r.json()





