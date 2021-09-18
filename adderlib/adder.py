import urllib.parse, typing
from .urlhandlers import UrlHandler, DebugHandler
from .users import AdderUser
from .devices import AdderReceiver, AdderTransmitter
from .channels import AdderChannel

class AdderRequestError(Exception):
	"""Adder API request has not returned success"""
	pass

class AdderAPI:
	"""Adderlink API for interacting with devices, channels, and users"""

	def __init__(self, url_handler:UrlHandler=None, user:AdderUser=None, api_version:int=8):
		self._user = user or AdderUser()
		self._url_handler = url_handler or DebugHandler()
		self._api_version = api_version

	# User authentication
	def login(self, username:str, password:str):
		"""Log the user in to the KVM system and retrieve an API token"""
		
		url = f"/api/?v={self._api_version}&method=login&username={urllib.parse.quote(username)}&password={urllib.parse.quote(password)}"
		response = self._url_handler.api_call(url)
		
		if response.get("success") == "1" and response.get("token") is not None:
			self._user.set_logged_in(username, response.get("token"))
	
	def logout(self) -> bool:
		"""Log the user out"""
		url = f"/api/?v={self._api_version}&token={self._user.token}&method=logout"
		response = self._url_handler.api_call(url)

		# TODO: More detailed error handling?
		# TODO: Maybe have the URL handler throw an exception?
		if response.get("success") == "1":
			self._user.set_logged_out()
		else:
			raise AdderRequestError()
	
	# Device management
	def getTransmitters(self) -> typing.Generator[AdderTransmitter, None, None]:
		"""Request a list of available Adderlink transmitters"""

		url = f"/api/?v={self._api_version}&token={self._user.token}&method=get_devices&device_type=tx"
		response = self._url_handler.api_call(url)

		if response.get("success") == "1" and "devices" in response:
			for device in response.get("devices").get("device"):
				if device.get("d_type") == "tx":
					yield AdderTransmitter(device)
			
	def getReceivers(self) -> typing.Generator[AdderReceiver, None, None]:
		"""Request a list of available Adderlink receivers"""

		url = f"/api/?v={self._api_version}&token={self._user.token}&method=get_devices&device_type=rx"
		response = self._url_handler.api_call(url)

		if response.get("success") == "1" and "devices" in response:			
			for device in response.get("devices").get("device"):
				if device.get("d_type") == "rx":
					yield AdderReceiver(device)
	
	# Channel management
	def getChannels(self) -> typing.Generator[AdderChannel, None, None]:
		"""Request a list of available Adderlink channels"""

		url = f"/api/?v={self._api_version}&token={self._user.token}&method=get_channels"
		response = self._url_handler.api_call(url)
		
		if response.get("success") == "1" and "channels" in response:
			for channel in response.get("channels").get("channel"):
				yield AdderChannel(channel)
	
	@property
	def user(self) -> AdderUser:
		"""Get the current user"""
		return self._user
	
	@property
	def transmitters(self) -> typing.Generator[AdderTransmitter]:
		"""Get all Adder transmitters"""
		return self.getTransmitters()
	
	@property
	def receivers(self) -> typing.Generator[AdderReceiver]:
		"""Get all Adder receivers"""
		return self.getReceivers()
	
	@property
	def channels(self) -> typing.Generator[AdderChannel]:
		"""Get all Adder channels"""
		return self.getChannels()