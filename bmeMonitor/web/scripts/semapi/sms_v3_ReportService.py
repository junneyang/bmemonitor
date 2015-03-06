#coding=utf-8
from ApiSDKJsonClient import *


class sms_v3_ReportService(ApiSDKJsonClient):

	def __init__(self):
		ApiSDKJsonClient.__init__(self, 'sms', 'v3', 'ReportService')

	def getRealTimeData(self, GetRealTimeDataRequest=None):
		return self.execute('getRealTimeData', GetRealTimeDataRequest)

	def getProfessionalReportId(self, GetProfessionalReportIdRequest=None):
		return self.execute('getProfessionalReportId', GetProfessionalReportIdRequest)

	def getReportState(self, GetReportStateRequest=None):
		return self.execute('getReportState', GetReportStateRequest)

	def getReportFileUrl(self, GetReportFileUrlRequest=None):
		return self.execute('getReportFileUrl', GetReportFileUrlRequest)

	def getRealTimeQueryData(self, GetRealTimeQueryDataRequest=None):
		return self.execute('getRealTimeQueryData', GetRealTimeQueryDataRequest)

	def getRealTimePairData(self, GetRealTimePairDataRequest=None):
		return self.execute('getRealTimePairData', GetRealTimePairDataRequest)



