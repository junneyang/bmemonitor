#coding=utf-8
from ApiSDKJsonClient import *


class sms_v3_FolderService(ApiSDKJsonClient):

	def __init__(self):
		ApiSDKJsonClient.__init__(self, 'sms', 'v3', 'FolderService')

	def getFolder(self, GetFolderRequest=None):
		return self.execute('getFolder', GetFolderRequest)

	def getMonitorWordByMonitorId(self, GetMonitorWordByMonitorIdRequest=None):
		return self.execute('getMonitorWordByMonitorId', GetMonitorWordByMonitorIdRequest)

	def getMonitorWordByFolderId(self, GetMonitorWordByFolderIdRequest=None):
		return self.execute('getMonitorWordByFolderId', GetMonitorWordByFolderIdRequest)

	def getMonitorWordByKeywordId(self, GetMonitorWordByKeywordIdRequest=None):
		return self.execute('getMonitorWordByKeywordId', GetMonitorWordByKeywordIdRequest)

	def addFolder(self, AddFolderRequest=None):
		return self.execute('addFolder', AddFolderRequest)

	def updateFolder(self, UpdateFolderRequest=None):
		return self.execute('updateFolder', UpdateFolderRequest)

	def deleteFolder(self, DeleteFolderRequest=None):
		return self.execute('deleteFolder', DeleteFolderRequest)

	def addMonitorWord(self, AddMonitorWordRequest=None):
		return self.execute('addMonitorWord', AddMonitorWordRequest)

	def deleteMonitorWord(self, DeleteMonitorWordRequest=None):
		return self.execute('deleteMonitorWord', DeleteMonitorWordRequest)



