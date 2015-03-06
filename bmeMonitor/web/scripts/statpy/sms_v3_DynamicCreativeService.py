#coding=utf-8
from ApiSDKJsonClient import *


class sms_v3_DynamicCreativeService(ApiSDKJsonClient):

	def __init__(self):
		ApiSDKJsonClient.__init__(self, 'sms', 'v3', 'DynamicCreativeService')

	def getExclusionTypeByCampaignId(self, GetExclusionTypeByCampaignIdRequest=None):
		return self.execute('getExclusionTypeByCampaignId', GetExclusionTypeByCampaignIdRequest)

	def addExclusionType(self, AddExclusionTypeRequest=None):
		return self.execute('addExclusionType', AddExclusionTypeRequest)

	def delExclusionType(self, DelExclusionTypeRequest=None):
		return self.execute('delExclusionType', DelExclusionTypeRequest)



