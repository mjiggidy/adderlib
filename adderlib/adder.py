import urllib.parse
from .urlhandlers import *
from .user import *
from .devices import *
from .channel import *


class AdderAPI:
	"""Adderlink API for interacting with devices, channels, and users"""

	def __init__(self, url_handler:UrlHandler=None, user:AdderUser=None, api_version:int=8):
		self.user = user or AdderUser()
		self._url_handler = url_handler or DebugHandler()
		self._api_version = api_version

	def login(self, username:str, password:str):
		"""Log the user in to the KVM system and retrieve an API token"""
		
		url = f"/api/?v={self._api_version}&method=login&username={urllib.parse.quote(username)}&password={urllib.parse.quote(password)}"
		response = self._url_handler.api_call(url)
		
		if response.get("success") == "1" and response.get("token") is not None:
			self.user.set_logged_in(username, response.get("token"))
	
	def getTransmitters(self):

		url = f"/api/?v={self._api_version}&token={self.user.token}&method=get_devices&device_type=tx"
		response = self._url_handler.api_call(url)

		if response.get("success") == "1" and "devices" in response:
			devices = response.get("devices")
			#print(devices.get("device"))
			
			
			for device in response.get("devices").get("device"):
				if device.get("d_type") == "tx":
					yield AdderTransmitter(device)
			
	def getReceivers(self):

		url = f"/api/?v={self._api_version}&token={self.user.token}&method=get_devices&device_type=rx"
		response = self._url_handler.api_call(url)

		if response.get("success") == "1" and "devices" in response:
			devices = response.get("devices")
			#print(devices.get("device"))
			
			
			for device in response.get("devices").get("device"):
				if device.get("d_type") == "rx":
					yield AdderReceiver(device)
	
	def getChannels(self):

		url = f"/api/?v={self._api_version}&token={self.user.token}&method=get_channels"
		response = self._url_handler.api_call(url)
		
		if response.get("success") == "1" and "channels" in response:
			channels = response.get("channels")

			for channel in channels.get("channel"):
				yield AdderChannel(channel)