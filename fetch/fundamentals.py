import requests
import json


class Scrape(object):
	'''Base class for scraping data from tickertape'''
	def __init__(self, sIds, user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"):
		self.sIds = sIds
		self._user_agent = user_agent

	'''getter setter for user_agent'''
	@property
	def user_agent(self):
		return self._user_agent

	@user_agent.setter
	def user_agent(self, url):
		self._user_agent = url

class FetchData(Scrape):
	'''Class to process and store fundamental data scraped from tickertape'''
	def __init__(self):
		super().__init__()