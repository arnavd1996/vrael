'''
Code to perform operations on loaded data for analysis
'''
import pandas as pd
from analyse.quant import QuantAnalyse
from math import log2

class LoadFrames:

	def __init__(self, tickers=pd.read_csv('data/info.csv').ticker.tolist(), dataLocation = 'data/YhistData'):
		
		redlist = pd.read_csv('data/redlist.csv',header=None)[0].tolist()

		self._tickers = [i for i in tickers if i not in redlist]		
		self._dataLocation = dataLocation
		self._Data = self.loadData()
		self._tradeDates = self.getTradeDates()

	#Getters for getting the dictionary named Data containing all the data, list of ticker names, trade dates
	@property
	def Data(self):
		return self._Data

	@property
	def Tickers(self):
		return self._tickers

	@property
	def tradeDates(self):
		return self._tradeDates

	def loadData(self):
		Data = {}
		for _ticker in self._tickers:
			df = pd.read_csv(f'{self._dataLocation}/{_ticker}.csv',index_col='Date')
			df = df.sort_index()
			df.index = pd.to_datetime(df.index)
			Data[_ticker] = df
		return Data

	def getTradeDates(self):
		data = self._Data
		tickers = list(data.keys())
		tradeDates = data[tickers[0]].index
		for ticker in tickers:
			tradeDates = tradeDates.union(data[ticker].index)
		return tradeDates

	def getSliceData(self,stDa,enDa):
		slicedData = {}
		for _ticker in self._tickers:
			df = self._Data[_ticker]
			df = df[(df.index>=stDa) & (df.index<=enDa)]
			slicedData[_ticker] = df
		return slicedData


class relativeFrames(LoadFrames):

	def __init__(self,currentDate,seed=5):
		super().__init__()
		self._currentDate = currentDate
		self._seed = seed

	@property
	def seed(self):
		return self._seed

	@seed.setter
	def seed(self, seed):
		self._seed = seed

	def getFrame(self):
		data = self._Data
		for ticker in self._tickers:
			df = data[ticker]
			prevDf = df[df.index<=currentDate]
			futureDf = df[df.index>currentDate]

	# Get  a list of windows of trading days before and after which are included in quant analysis
	def windows(self,df):
		length = len(df.index)
		print(length)
		maxPower = int(log2(length/self._seed))
		windows = []
		for n in range(maxPower+1):
			windows.append(self._seed*2**n)
		return windows





