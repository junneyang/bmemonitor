#coding=utf-8
from ApiSDKJsonClient import *


class sms_v3_CreativeService(ApiSDKJsonClient):

	def __init__(self):
		ApiSDKJsonClient.__init__(self, 'sms', 'v3', 'CreativeService')

	def addCreative(self, AddCreativeRequest=None):
		return self.execute('addCreative', AddCreativeRequest)

	def updateCreative(self, UpdateCreativeRequest=None):
		return self.execute('updateCreative', UpdateCreativeRequest)

	def activateCreative(self, ActivateCreativeRequest=None):
		return self.execute('activateCreative', ActivateCreativeRequest)

	def deleteCreative(self, DeleteCreativeRequest=None):
		return self.execute('deleteCreative', DeleteCreativeRequest)

	def getCreativeIdByAdgroupId(self, GetCreativeIdByAdgroupIdRequest=None):
		return self.execute('getCreativeIdByAdgroupId', GetCreativeIdByAdgroupIdRequest)

	def getCreativeByAdgroupId(self, GetCreativeByAdgroupIdRequest=None):
		return self.execute('getCreativeByAdgroupId', GetCreativeByAdgroupIdRequest)

	def getCreativeByCreativeId(self, GetCreativeByCreativeIdRequest=None):
		return self.execute('getCreativeByCreativeId', GetCreativeByCreativeIdRequest)

	def getCreativeStatus(self, GetCreativeStatusRequest=None):
		return self.execute('getCreativeStatus', GetCreativeStatusRequest)

	def getCreativeStatusZip(self, GetCreativeStatusZipRequest=None):
		return self.execute('getCreativeStatusZip', GetCreativeStatusZipRequest)



