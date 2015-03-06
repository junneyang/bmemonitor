#coding=utf-8
from ApiSDKJsonClient import *


class sms_v3_CampaignService(ApiSDKJsonClient):

	def __init__(self):
		ApiSDKJsonClient.__init__(self, 'sms', 'v3', 'CampaignService')

	def getAllCampaignId(self, GetAllCampaignIdRequest=None):
		return self.execute('getAllCampaignId', GetAllCampaignIdRequest)

	def getCampaignByCampaignId(self, GetCampaignByCampaignIdRequest=None):
		return self.execute('getCampaignByCampaignId', GetCampaignByCampaignIdRequest)

	def getAllCampaign(self, GetAllCampaignRequest=None):
		return self.execute('getAllCampaign', GetAllCampaignRequest)

	def addCampaign(self, AddCampaignRequest=None):
		return self.execute('addCampaign', AddCampaignRequest)

	def updateCampaign(self, UpdateCampaignRequest=None):
		return self.execute('updateCampaign', UpdateCampaignRequest)

	def deleteCampaign(self, DeleteCampaignRequest=None):
		return self.execute('deleteCampaign', DeleteCampaignRequest)



