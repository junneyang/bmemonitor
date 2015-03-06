#coding=utf-8
import suds
import sys
import ConfigParser
import traceback as tb

'''
    webservice client
'''
class ApiSDKSoapClient():
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
    __client=None
    
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
            self.__username=ApiSDKSoapClient.usernameconf
            self.__password=ApiSDKSoapClient.passwordconf
            self.__token=ApiSDKSoapClient.tokenconf
            self.__target=ApiSDKSoapClient.targetconf
            self.__action=ApiSDKSoapClient.actionconf
        except Exception, e:
            print e
            tb.print_exc()
            
    def initConfig(self):
        if (ApiSDKSoapClient.actionconf==None):
            cf = ConfigParser.ConfigParser()
            cf.read("baidu-api.properties")
            ApiSDKSoapClient.urlconf=cf.get("api", "serverUrl")
            ApiSDKSoapClient.usernameconf=cf.get("api", "username")
            ApiSDKSoapClient.passwordconf=cf.get("api", "password")
            ApiSDKSoapClient.tokenconf=cf.get("api", "token")
            ApiSDKSoapClient.targetconf=cf.get("api", "target")
            ApiSDKSoapClient.actionconf=cf.get("api", "action")
            
    def newSoapClient(self):
        try:
            url = self.__url + '/sem/'+self.__productline+'/'+self.__version+'/' + self.__service + '?wsdl'
            self.__client = suds.client.Client(url)
            header = self.__client.factory.create('ns0:AuthHeader')
            header.username = self.__username
            header.password = self.__password
            header.token = self.__token
            header.target = self.__target
            header.action = self.__action
            header.accessToken = self.__accessToken
            self.__client.set_options(soapheaders=header)
            return self.__client
        except Exception, e:
            print e
            tb.print_exc()
            
    def getSoapClient(self):
        if (self.__client==None):
            self.newSoapClient()
        return  self.__client
    
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
def printSoapResponse(res):
        resheader = res.getChild("Envelope").getChild("Header").getChild("ResHeader")
        resbody = res.getChild("Envelope").getChild("Body")
        failures = resheader.getChild("failures")
        print "Response Header=>"
        print "Execution result: \t", resheader.getChild("desc").getText()
        print "      operations: \t", resheader.getChild("oprs").getText()
        print "  operation time: \t", resheader.getChild("oprtime").getText()
        if (resheader.getChild("quota")!=None):
            print "   consume quota: \t", resheader.getChild("quota").getText()
            
        if (resheader.getChild("rquota")!=None):
            print "    remain quota: \t", resheader.getChild("rquota").getText()
            
        print "          status: \t", resheader.getChild("status").getText()
        if failures is not None:
            print "            code: \t", failures.getChild("code").getText()
            print "         message: \t", failures.getChild("message").getText()
            print "        position: \t", failures.getChild("position").getText();
        print "Response Body=>"
        if resbody is not None:
            print resbody



