#coding=utf-8
from ApiSDKJsonClient import *


class sms_v3_BulkJobService(ApiSDKJsonClient):

	def __init__(self):
		ApiSDKJsonClient.__init__(self, 'sms', 'v3', 'BulkJobService')

	def getFileState(self, GetFileStateRequest=None):
		return self.execute('getFileState', GetFileStateRequest)

	def getAllChangedObjects(self, GetAllChangedObjectsRequest=None):
		return self.execute('getAllChangedObjects', GetAllChangedObjectsRequest)

	def getChangedItemId(self, GetChangedItemIdRequest=None):
		return self.execute('getChangedItemId', GetChangedItemIdRequest)

	def getFilePath(self, GetFilePathRequest=None):
		return self.execute('getFilePath', GetFilePathRequest)

	def getChangedCampaignId(self, GetChangedCampaignIdRequest=None):
		return self.execute('getChangedCampaignId', GetChangedCampaignIdRequest)

	def getChangedId(self, GetChangedIdRequest=None):
		return self.execute('getChangedId', GetChangedIdRequest)

	def getChangedNewCreativeId(self, GetChangedNewCreativeIdRequest=None):
		return self.execute('getChangedNewCreativeId', GetChangedNewCreativeIdRequest)

	def getChangedScale(self, GetChangedScaleRequest=None):
		return self.execute('getChangedScale', GetChangedScaleRequest)

	def getAllObjects(self, GetAllObjectsRequest=None):
		return self.execute('getAllObjects', GetAllObjectsRequest)

	def getChangedAdgroupId(self, GetChangedAdgroupIdRequest=None):
		return self.execute('getChangedAdgroupId', GetChangedAdgroupIdRequest)

	def getSelectedObjects(self, GetSelectedObjectsRequest=None):
		return self.execute('getSelectedObjects', GetSelectedObjectsRequest)

	def cancelDownload(self, CancelDownloadRequest=None):
		return self.execute('cancelDownload', CancelDownloadRequest)



