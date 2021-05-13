'''
Code to perform quant analysis on dataframes
'''
import pandas as pd
from ta.volatility import BollingerBands
from ta.trend import ADXIndicator
from ta.momentum import RSIIndicator
from ta.volume import MFIIndicator, AccDistIndexIndicator


class QuantAnalyse:
	def __init__(self,df,boll=True,rsi=True,mfi=True,adx=True,accdi=True):
		self._df = df
		self._boll = boll
		self._rsi = rsi
		self._mfi = mfi
		self._adx = adx
		self._accdi = accdi

	def addIndicators(self,window):
		df = self._df

		if (len(df.index)<=(window+2)):
			raise Exception("Please ensure window size is 3 more than number of dataframe rows")

		if self._boll:
			boll  =  BollingerBands(close = df.Close, window = window, window_dev = 2)
			boll = boll.bollinger_pband()
			boll.name = f'{window}_boll'
			df = df.join(boll) 

		if self._rsi:
			rsi = RSIIndicator(close = df.Close, window = window)
			rsi = rsi.rsi()
			rsi.name = f'{window}_RSI'
			df = df.join(rsi)

		if self._mfi:
			mfi = MFIIndicator(high = df.High,low = df.Low,close = df.Close,volume = df.Volume)
			mfi = mfi.money_flow_index()
			mfi.name = f'{window}_MFI'
			df = df.join(mfi)

		if self._adx:
			ad = ADXIndicator(high = df.High, low = df.Low, close = df.Close, window = window)
			# df['ADXPos'] = ad.adx_pos()
			# df['ADXNeg'] = ad.adx_neg()
			ad = ad.adx()
			ad.name = f'{window}_ADX'
			df = df.join(ad)

		if self._accdi:
			accdi = AccDistIndexIndicator(high = df.High, low = df.Low, close = df.Close, volume = df.Volume)
			accdi = accdi.acc_dist_index()
			accdi.name = f'{window}_AccDi'

		return df