'''
Code to perform operations on loaded data for analysis
'''
import pandas as pd

class LoadFrames:

	def __init__(self, tickers=pd.read_csv('data/info.csv').ticker.tolist(), dataLocation = 'data/YhistData'):
		
		redlist = pd.read_csv('data/redlist.csv',header=None)[0].tolist()

		self._tickers = [i for i in tickers if i not in redlist]		
		self._dataLocation = dataLocation
		self._Data = self.loadData()


	def loadData(self):

		Data = {}

		for _ticker in self._tickers:
			df = pd.read_csv(f'{self._dataLocation}/{_ticker}.csv',index_col='Date')
			df = df.sort_index()
			df.index = pd.to_datetime(df.index)
			Data[_ticker] = df

		return Data

	#Getter for getting the dictionary named Data containing all the data
	@property
	def Data(self):
		return self._Data

class SlicedFrames(LoadFrames):

	def __init__(self,stDa,enDa):
		super().__init__()
		self._stDa = stDa
		self._enDa = enDa
		self._slicedData = self.slice()

	#Getter for getting the dictionary named slicedData containing all the data
	@property
	def slicedData(self):
		return self._slicedData

	def slice(self):
		slicedData = {}
		for _ticker in self._tickers:
			df = self._Data[_ticker]
			df = df[(df.index>=self._stDa) & (df.index<=self._enDa)]
			slicedData[_ticker] = df
		return slicedData