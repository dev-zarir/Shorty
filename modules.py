from requests import get
from json import loads
from datetime import datetime
from pytz import timezone
from requests.exceptions import ConnectionError, ConnectTimeout

def getip():
	success=False
	while not success:
		try:
			ip = get('https://api.ipify.org').text
			success=True
		except ConnectionError:
			continue
		except ConnectTimeout:
			continue
	return ip

class user_info:
	def __init__(self):
		self.info=loads(get('https://ipinfo.io/json').text)
	@property
	def ip(self):

		return self.info['ip']
	@property
	def city(self):

		return self.info['city']
	@property
	def region(self):

		return self.info['region']
	@property
	def country(self):

		return self.info['country']
	@property
	def postal(self):

		return self.info['postal']
	@property
	def timezone(self):

		return self.info['timezone']
	@property
	def date(self):

		date=datetime.now(timezone(self.info['timezone'])).strftime('%d-%m-%Y')
		return date
	@property
	def time(self):

		time=datetime.now(timezone(self.info['timezone'])).strftime('%I:%M:%S %p')
		return time
	@property
	def full_time(self):

		date=datetime.now(timezone(self.info['timezone'])).strftime('%d-%m-%Y')
		time=datetime.now(timezone(self.info['timezone'])).strftime('%I:%M:%S %p')
		fulltime=time+' on '+date
		return fulltime

