#coding=utf-8
from ApiSDKJsonClient import *


class sms_v3_AccountService(ApiSDKJsonClient):

	def __init__(self):
		ApiSDKJsonClient.__init__(self, 'sms', 'v3', 'AccountService')

	def getAccountInfo(self, GetAccountInfoRequest=None):
		return self.execute('getAccountInfo', GetAccountInfoRequest)

	def updateAccountInfo(self, UpdateAccountInfoRequest=None):
		return self.execute('updateAccountInfo', UpdateAccountInfoRequest)



