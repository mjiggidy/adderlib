import abc, urllib.parse, enum
import xmltodict
from datetime import datetime
from dataclasses import dataclass

class UrlHandler(abc.ABC):

	@classmethod
	@abc.abstractmethod
	def api_call(url) -> dict:
		pass
"""
class RequestsHandler(UrlHandler):
	
	import requests

	@classmethod
	def api_call(url) -> dict:
		response = requests.get(url)
		if response.ok:
			return response.content
"""

class DebugHandler(UrlHandler):

	@classmethod
	def api_call(cls, url) -> dict:

		params = urllib.parse.parse_qs(url)
		print(f"Requesting: {url}")
		print(f"With params: {params}")
		
		method = params.get("method")[0]

		if method == "login":
			if params.get("password")[0] == "goodpwd":
				with open("example_xml/login.xml") as api_response:
					response = xmltodict.parse(api_response.read()).get("api_response")
				return response
			else:
				with open("example_xml/login_fail.xml") as api_response:
					response = xmltodict.parse(api_response.read()).get("api_response")
				return response
		
		elif method == "get_devices":
			with open("example_xml/get_devices.xml") as api_response:
				response = xmltodict.parse(api_response.read()).get("api_response")
			#	print("Responding with",response)
			return response

		

class AdderDevice(abc.ABC):

	@enum.unique
	class DeviceType(enum.Enum):
		"""Types of Adder devices"""
		RX = 0
		TX = 1
	
	@enum.unique
	class DeviceStatus(enum.Enum):
		"""Operational status of Adder device"""
		UNKNOWN			= -1
		OFFLINE         =  0
		ONLINE          =  1
		REBOOTING       =  2
		UPGRADING       =  4
		BACKUP_FIRMWARE =  6
	
	@enum.unique
	class DeviceModel(enum.Enum):
		"""AdderLink device models"""
		UNKNOWN  = -1
		ALIF1000 =  0
		ALIF2002 =  1
		ALIF2112 =  2
		ALIF1002 =  3
		ALIF2020 =  4 
	

	@dataclass
	class NetworkInterface:
		"""Network interface info"""
		ip_address:str
		mac_address:str
		is_online:bool
	
	def __init__(self, properties:dict):
		self._extended = {key: val for key,val in properties.items()}
	
	# Human-friendly descriptions
	@property
	def name(self) -> str:
		"""Device name"""
		return self._extended.get("d_name") or None

	@property
	def description(self) -> str:
		"""Device description"""
		return self._extended.get("d_description") or None

	@property
	def location(self) -> str:
		"""Device location"""
		return self._extended.get("d_location") or None
	
	@property
	def date_dadded(self) -> datetime:
		"""The date/time this device was set up"""
		return datetime.fromisoformat(self._extended.get("d_date_added"))
	

	# Addresses and IDs
	@property
	def id(self) -> str:
		"""Device ID"""
		return self._extended.get("d_id") or None	
	
	@property
	def serial_number(self) -> str:
		"""Device serial number"""
		return self._extended.get("d_serial_number") or None
	
	@property
	def ip_addresses(self) -> tuple():
		"""IP addresses on the network"""
		return (self._extended.get("d_ip_address") or None, self._extended.get("d_ip_address2") or None)
	
	@property
	def ip_address(self) -> str:
		"""Primary IP address of the device"""
		return self.ip_addresses[0] or None

	@property
	def mac_addresses(self) -> tuple():
		"""MAC addresses of the interfaces"""
		return (self._extended.get("d_mac_address") or None, self._extended.get("d_mac_address2") or None)
	
	@property
	def mac_address(self) -> str:
		"""Primary MAC address"""
		return self.mac_addresses[0]

	@property
	def interfaces(self) -> tuple():
		"""Return network interfaces"""
		return (
			self.NetworkInterface(self.ip_addresses[0], self.mac_addresses[0], int(self._extended.get("d_online",-1))>0),
			self.NetworkInterface(self.ip_addresses[1], self.mac_addresses[1], int(self._extended.get("d_online2",-1))>0)
		)

	# Firmware verions
	@property
	def firmware(self) -> str:
		"""Current firmware version"""
		return self._extended.get("d_firmware") or None
	
	@property
	def backup_firmware(self) -> str:
		"""Backup firmware version"""
		return self._extended.get("d_backup_firmware") or None
	
	# Status
	@property
	def status(self) -> DeviceStatus:
		"""Device status"""
		try:
			return self.DeviceStatus(int(self._extended.get("d_status")))
		except Exception as e:
			return self.DeviceStatus(-1)

	@property
	def is_configured(self) -> bool:
		"""If the device has been set up"""
		return int(self._extended.get("d_configured",0)) > 0
	
	@property
	def is_firmware_valid(self) -> bool:
		"""If the current firmware is in working order"""
		return int(self._extended.get("d_valid_firmware")) > 0
	
	@property
	def is_backup_firmware_valid(self) -> bool:
		"""If the current firmware is in working order"""
		return int(self._extended.get("d_valid_backup_firmware")) > 0
	
	@property
	def model(self) -> DeviceModel:
		"""Device model"""
		if self._extended.get("d_version") == '1':
			return self.DeviceModel.ALIF1000
		
		elif self._extended.get("d_variant") == 'b':
			return self.DeviceModel.ALIF2002

		elif self._extended.get("d_variant") == 'v':
			return self.DeviceModel.ALIF2002
		
		elif self._extended.get("d_variant") == 's':
			return self.DeviceModel.ALIF1002

		elif self._extended.get("d_variant") == 't':
			return self.DeviceModel.ALIF2020
		
		else:
			return self.DeviceModel.UNKNOWN

	@property
	@abc.abstractmethod
	def type(self) -> DeviceType:
		"""Type of Adder device"""
		pass

class AdderTransmitter(AdderDevice):
	"""Adderlink Transmitter (TX) Device"""

	@property
	def channel_count(self) -> int:
		"""Number of channels that use this device"""
		return int(self._extended.get("count_transmitter_channels"))
	
	@property
	def preset_count(self) -> int:
		"""Number of presets that use this device"""
		return int(self._extended.get("count_transmitter_presets"))

	@property
	def type(self) -> AdderDevice.DeviceType:
		return AdderDevice.DeviceType.TX


class AdderReceiver(AdderDevice):
	"""Adderlink Receiver (RX) Device"""


	@property
	def type(self) -> AdderDevice.DeviceType:
		return AdderDevice.DeviceType.RX


class AdderUser:
	"""Authenticated user"""

	def __init__(self):
		self._logged_in = False
		self._username = None
		self._token = None
	
	def set_logged_in(self, user:str, token:str):
		"""Log a user in with a valid session token"""
		self._username = user
		self._token = token
	
	def set_logged_out(self):
		"""Log the user out"""
		self._username = None
		self._token = None

	@property
	def logged_in(self) -> bool:
		return True if self._username and self._token else False
	
	@property
	def logged_out(self) -> bool:
		return not self.logged_in
	
	@property
	def username(self) -> str:
		return self._username
	
	@property
	def token(self) -> str:
		return self._token


class AdderAPI:

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
				#print("Device:",device)
				yield AdderTransmitter(device)
			
	
	
