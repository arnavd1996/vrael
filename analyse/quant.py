'''
Code to perform quant analysis on dataframes
'''
import pandas as pd
from ta.volatility import BollingerBands
from ta.trend import ADXIndicator,adx
from ta.momentum import RSIIndicator
from ta.volume import MFIIndicator, AccDistIndexIndicator


class QuantAnalyse:
	def __init__(self,df,boll=True,rsi=True,mfi=True,adx=True,accdi=True,ret=True):
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
			bollp = boll.bollinger_pband()
			bollw = boll.bollinger_wband()
			bollp.name = f'bollp_{window}'
			bollw.name = f'bollw_{window}'
			df = df.join(bollp)
			df = df.join(bollw)

		if self._rsi:
			rsi = RSIIndicator(close = df.Close, window = window)
			rsi = rsi.rsi()
			rsi.name = f'RSI_{window}'
			df = df.join(rsi)

		if self._mfi:
			mfi = MFIIndicator(high = df.High,low = df.Low,close = df.Close,volume = df.Volume)
			mfi = mfi.money_flow_index()
			mfi.name = f'MFI_{window}'
			df = df.join(mfi)

		if self._adx:
			ad = ADXIndicator(high = df.High, low = df.Low, close = df.Close, window = window)
			adp = ad.adx_pos()
			adn = ad.adx_neg()
			adp.name = f'ADXp_{window}'
			adn.name = f'ADXn_{window}'
			df = df.join(adp)
			df = df.join(adn)

		if self._accdi:
			accdi = AccDistIndexIndicator(high = df.High, low = df.Low, close = df.Close, volume = df.Volume)
			accdi = accdi.acc_dist_index()
			accdi.name = f'AccDi_{window}'
			df = df.join(accdi)

		return df


	def checkIndicators(self):
		indicators = []

		if self._boll:
			indicators.append('bollp')
			indicators.append('bollw')

		if self._rsi:
			indicators.append('RSI')

		if self._mfi:
			indicators.append('MFI')

		if self._adx:
			indicators.append('ADXp')
			indicators.append('ADXn')

		if self._accdi:
			indicators.append('AccDi')

		return indicators



	def oneDIndicators(self,window):
		df = self.addIndicators(window)
		out = {}

		currentPrice = df.Close.iloc[-1]
		prevPrice = df.Close.iloc[-1*window]
		out[f'return_{window}'] = ((currentPrice-prevPrice)/prevPrice)*100

		indicators = self.checkIndicators()

		for indicator in indicators:
			out[f'{indicator}_{window}'] = df[f'{indicator}_{window}'].iloc[-1]

		return out