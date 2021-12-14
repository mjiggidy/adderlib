import urllib.parse, typing

from .urlhandlers import UrlHandler, DebugHandler, RequestsHandler
from .users import AdderUser
from .devices import AdderReceiver, AdderTransmitter
from .channels import AdderChannel
from .presets import AdderPreset

class AdderRequestError(Exception):
	"""Adder API request has not returned success"""
	pass

class AdderAPI:

	def __init__(self,*,url_handler:typing.Optional[UrlHandler]=None, user:typing.Optional[AdderUser]=None, api_version:typing.Optional[int]=8):
		"""Adderlink API for interacting with devices, channels, and users"""
		self.setUser(user or AdderUser())
		self.setUrlHandler(url_handler or RequestsHandler())
		self.setApiVersion(api_version)

	# User authentication
	def login(self, username:str, password:str):
		"""Log the user in to the KVM system and retrieve an API token"""
		
		url = f"/api/?v={self._api_version}&method=login&username={urllib.parse.quote(username)}&password={urllib.parse.quote(password)}"
		response = self._url_handler.api_call(url)
		
		if response.get("success") == "1" and response.get("token") is not None:
			self._user.set_logged_in(username, response.get("token"))
	
	def logout(self):
		"""Log the user out"""
		url = f"/api/?v={self._api_version}&token={self._user.token}&method=logout"
		response = self._url_handler.api_call(url)

		# TODO: More detailed error handling?
		# TODO: Maybe have the URL handler throw an exception?
		if response.get("success") == "1":
			self._user.set_logged_out()
		else:
			raise AdderRequestError()
		
	def setUrlHandler(self, handler:UrlHandler):
		"""Set the UrlHandler to use for AdderAPI URL calls"""
		if not isinstance(handler, UrlHandler):
			raise ValueError(f"URL handler {type(handler)} is not an instance of UrlHandler")
		self._url_handler = handler
	
	def setUser(self, user:AdderUser):
		"""Set the AdderUser to use for AdderAPI calls"""
		if not isinstance(user, AdderUser):
			raise ValueError(f"User type{type(user)} is not an instance of AdderUser")
		self._user = user
	
	def setApiVersion(self, version:int):
		"""Set the API version to use"""
		self._api_version = int(version)
	
	# Device management
	def getTransmitters(self, t_id:typing.Optional[int]=None) -> typing.Generator[AdderTransmitter, None, None]:
		"""Request a list of available Adderlink transmitters"""

		url = f"/api/?v={self._api_version}&token={self._user.token}&method=get_devices&device_type=tx"

		if t_id is not None:
			url += f"&filter_t_id={t_id}"

		response = self._url_handler.api_call(url)

		if response.get("success") == "1" and "devices" in response:
			for device in response.get("devices").get("device"):
				yield AdderTransmitter(device)
			
	def getReceivers(self) -> typing.Generator[AdderReceiver, None, None]:
		"""Request a list of available Adderlink receivers"""

		url = f"/api/?v={self._api_version}&token={self._user.token}&method=get_devices&device_type=rx"
		response = self._url_handler.api_call(url)

		if response.get("success") == "1" and "devices" in response:			
			for device in response.get("devices").get("device"):
				yield AdderReceiver(device)
	
	# Channel management
	def getChannels(self) -> typing.Generator[AdderChannel, None, None]:
		"""Request a list of available Adderlink channels"""

		url = f"/api/?v={self._api_version}&token={self._user.token}&method=get_channels"
		response = self._url_handler.api_call(url)
		
		if response.get("success") == "1" and "channels" in response:
			for channel in response.get("channels").get("channel"):
				yield AdderChannel(channel)
	
	def connectToChannel(self, channel:AdderChannel, receiver:AdderReceiver, mode:typing.Optional[AdderChannel.ConnectionMode]=AdderChannel.ConnectionMode.SHARED) -> bool:
		"""Connect a channel to a receiver"""

		url = f"/api/?v={self._api_version}&token={self._user.token}&method=connect_channel&c_id={channel.id}&rx_id={receiver.id}&mode={mode.value}"
		response = self._url_handler.api_call(url)
		if response.get("success") == "1":
			return True
		
		elif "errors" in response:
			for error in response.get("errors").get("error"):
				raise Exception(f"Error {error.get('code','?')}: {error.get('msg','?')}")
		
		else:
			raise Exception("Unknown error")
	
	# Preset management
	def getPresets(self) -> typing.Generator[AdderPreset, None, None]:
		"""Request a list of available Adderlink presets"""

		url = f"/api/?v={self._api_version}&token={self._user.token}&method=get_presets"
		response = self._url_handler.api_call(url)
		
		if response.get("success") == "1" and "connection_preset" in response:
			for preset in response.get("connection_preset"):
				yield AdderPreset(preset)	
	
	@property
	def user(self) -> AdderUser:
		"""Get the current user"""
		return self._user
	
	@property
	def url_handler(self) -> UrlHandler:
		"""Get the URL Handler"""
		return self._url_handler
	
	@property
	def transmitters(self) -> typing.Generator[AdderTransmitter, None, None]:
		"""Get all Adder transmitters"""
		return self.getTransmitters()
	
	@property
	def receivers(self) -> typing.Generator[AdderReceiver, None, None]:
		"""Get all Adder receivers"""
		return self.getReceivers()
	
	@property
	def channels(self) -> typing.Generator[AdderChannel, None, None]:
		"""Get all Adder channels"""
		return self.getChannels()