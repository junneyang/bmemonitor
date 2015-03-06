#coding=utf-8
from ApiSDKJsonClient import *


class sms_v3_KRService(ApiSDKJsonClient):

	def __init__(self):
		ApiSDKJsonClient.__init__(self, 'sms', 'v3', 'KRService')

	def getAdGroupBySeedWords(self, GetAdGroupBySeedWordsRequest=None):
		return self.execute('getAdGroupBySeedWords', GetAdGroupBySeedWordsRequest)

	def getKRbySeedWord(self, GetKRbySeedWordRequest=None):
		return self.execute('getKRbySeedWord', GetKRbySeedWordRequest)

	def getKRFileIdbySeedWord(self, GetKRFileIdbySeedWordRequest=None):
		return self.execute('getKRFileIdbySeedWord', GetKRFileIdbySeedWordRequest)

	def getKRFileState(self, GetKRFileStateRequest=None):
		return self.execute('getKRFileState', GetKRFileStateRequest)

	def getKRFilePath(self, GetKRFilePathRequest=None):
		return self.execute('getKRFilePath', GetKRFilePathRequest)

	def getKRQuota(self, GetKRQuotaRequest=None):
		return self.execute('getKRQuota', GetKRQuotaRequest)

	def getKRbySeedUrl(self, GetKRbySeedUrlRequest=None):
		return self.execute('getKRbySeedUrl', GetKRbySeedUrlRequest)

	def getSeedWord(self, GetSeedWordRequest=None):
		return self.execute('getSeedWord', GetSeedWordRequest)

	def getSeedUrl(self, GetSeedUrlRequest=None):
		return self.execute('getSeedUrl', GetSeedUrlRequest)

	def getKRCustom(self, GetKRCustomRequest=None):
		return self.execute('getKRCustom', GetKRCustomRequest)

	def getKRByMultiSeedWord(self, GetKRByMultiSeedWordRequest=None):
		return self.execute('getKRByMultiSeedWord', GetKRByMultiSeedWordRequest)



