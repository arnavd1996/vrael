'''
Code to fetch price data from yahoo finance
'''

import pandas as pd
import yfinance as yf
import numpy as np

class FetchPrice:
	'''
	interval:
		fetch data by interval (including intraday if period < 60 days)
		valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
		(optional, default is '1d')
	period:
		use "period" instead of start/end
		valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
		(optional, default is '1mo')
	location:
		location where the data is to be stored
	exchange:
		NS for NSE, BO for BSE
	'''
	def __init__(self,interval='1d',period='max',location='data/YhistData',exchange='NS'):
		self._interval = interval
		self._period = period
		self._location = location
		self._exchange = exchange

	'''
	input: tickers - list of tickers for which data is to be fetched
			redLocation - Location to store names of companies with no data returned
	output: csv file containing entire historical data stored in location
			redlist - csv file containing names of companies with no data returned by yfinance
	'''
	def store(self,tickers=pd.read_csv('data/info.csv').ticker.tolist(),redLocation = 'data/redlist'):

		#List to store companies giving no output data
		redlist = []

		#Code to fetch NSE stock price data from yfinance and store it at location
		for i,ticker in enumerate(tickers):		
			data = yf.Ticker(f'{ticker}.{self._exchange}')
			histData = data.history(interval=self._interval,period=self._period)
			if histData.empty:
				redlist.append(ticker)
			else:
				histData.index = pd.to_datetime(histData.index)
				histData = histData.sort_index()
				print(i,ticker)
				histData.to_csv(f'{self._location}/{ticker}.csv')

		pd.Series(redlist).to_csv(f'{redLocation}.csv',index=False,header=False)
		
		return	





		