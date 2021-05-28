import abc, urllib.parse, enum
from typing import ValuesView
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
		
		elif method == "get_channels":
			with open("example_xml/get_channels.xml") as api_response:
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
		return self.mac_addresses[0] or None

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
	def device_type(self) -> DeviceType:
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
	def device_type(self) -> AdderDevice.DeviceType:
		return AdderDevice.DeviceType.TX


class AdderReceiver(AdderDevice):
	"""Adderlink Receiver (RX) Device"""

	# TODO: con_exclusive(bool) vs count_control(enum) for determining exclusive mode?

	@enum.unique
	class ConnectionControlType(enum.Enum):
		"""Control modes"""
		UNKNOWN    = -1
		VIDEO_ONLY =  1
		EXCLUSIVE  =  2
		SHARED     =  3

	@property
	def device_type(self) -> AdderDevice.DeviceType:
		return AdderDevice.DeviceType.RX
	
	# Connection info

	@property
	def connection_start(self) -> datetime:
		"""Time the last known connection started"""
		return datetime.fromisoformat(self._extended.get("con_start_time"))
		
	@property
	def connection_end(self) -> datetime:
		"""Time the last known connection was ended.  Returns None if connection is current."""
		if self._extended.get("con_end_time") is not None:
			return datetime.fromisoformat(self._extended.get("con_end_time"))
		else:
			return None

	@property
	def connection_control(self) -> ConnectionControlType:
		"""Control mode of the last known connection"""
		con_type = int(self._extended.get("con_control", -1))
		if con_type in range(1,4):
			return self.ConnectionControlType(con_type)
		else:
			return self.ConnectionControlType(-1)
	
	@property
	def channel_name(self) -> str:
		"""The name of the last known channel this receiver was connected"""
		return self._extended.get("c_name")

	@property
	def is_connected(self) -> bool:
		"""Is the receiver currently connected to a channel"""
		return self.connection_start and self.connection_end
	
	# Connected user info

	@property
	def last_username(self) -> str:
		"""Last known username"""
		return self._extended.get("u_username") or None
	
	@property
	def last_userid(self) -> int:
		"""Last known user ID"""
		return int(self._extended.get("u_userid"))
	
	# Stats

	@property
	def group_count(self) -> int:
		"""Number of receiver groups this belongs to"""
		return int(self._extended.get("count_receiver_groups"))

	@property
	def preset_count(self) -> int:
		"""Number of receiver presets this belongs to"""
		return int(self._extended.get("count_receiver_presets"))
	
	@property
	def user_count(self) -> int:
		"""Number of users with access to this receiver"""
		return int(self._extended.get("count_users")) 

	
	
class AdderChannel:

	@enum.unique
	class ButtonState(enum.Enum):
		"""Video-only mode capabilities"""
		UNKNOWN  = -1
		DISABLED =  0	# No, because something is in use by someone else
		ENABLED  =  1	# Yes
		HIDDEN   =  2	# Never

	def __init__(self, properties:dict):
		self._extended = {key: val for key,val in properties.items()}
	
	@property
	def id(self) -> str:
		"""Channel ID"""
		return self._extended.get("c_id") or None
	
	@property
	def name(self) -> str:
		"""Channel name"""
		return self._extended.get("c_name")
	
	@property
	def description(self) -> str:
		"""Channel description"""
		return self._extended.get("c_description")
	
	@property
	def location(self) -> str:
		"""Channel location"""
		return self._extended.get("c_location")
	
	@property
	def type(self) -> str:
		"""Channel type"""
		# TODO: Investigate.  Not in the documentation
		return self._extended.get("c_channel_type")

	@property
	def tx_id(self) -> str:
		"""Device ID"""
		# TODO: Investigate.  Not in the documentation
		return self._extended.get("c_tx_id") or None
	
	@property
	def is_online(self) -> bool:
		"""Device status"""
		# TODO: Investigate.  Not in the documentation
		return self._extended.get("channel_online") == "true"
	
	@property
	def is_favorite(self) -> bool:
		"""Whether the channel has been favorited"""
		return self._extended.get("c_favourite") != "false"
	
	@property
	def shortcut(self) -> int:
		"""Returns the shortcut index if set, otherwise returns None"""
		pre = self._extended.get("c_favorite","")
		return int(pre) if pre.isnumeric() else None
	
	@property
	def view_button(self) -> ButtonState:
		"""Indicates the state of the video-only view button"""
		state = self._extended.get("view_button")
		if state == "disabled":
			return self.ButtonState.DISABLED
		elif state == "enabled":
			return self.ButtonState.ENABLED
		elif state == "hidden":
			return self.ButtonState.HIDDEN
		else:
			return self.ButtonState.UNKNOWN
	
	@property
	def shared_button(self) -> ButtonState:
		"""Indicates the state of the shared view button"""
		state = self._extended.get("shared_button")
		if state == "disabled":
			return self.ButtonState.DISABLED
		elif state == "enabled":
			return self.ButtonState.ENABLED
		elif state == "hidden":
			return self.ButtonState.HIDDEN
		else:
			return self.ButtonState.UNKNOWN

	@property
	def control_button(self) -> ButtonState:
		"""Indicates the state of the full-control button"""
		state = self._extended.get("control_button")
		if state == "disabled":
			return self.ButtonState.DISABLED
		elif state == "enabled":
			return self.ButtonState.ENABLED
		elif state == "hidden":
			return self.ButtonState.HIDDEN
		else:
			return self.ButtonState.UNKNOWN

	@property
	def exclusive_button(self) -> ButtonState:
		"""Indicates the state of the video-only view button"""
		state = self._extended.get("exclusive_button")
		if state == "disabled":
			return self.ButtonState.DISABLED
		elif state == "enabled":
			return self.ButtonState.ENABLED
		elif state == "hidden":
			return self.ButtonState.HIDDEN
		else:
			return self.ButtonState.UNKNOWN
	
	@property
	def view_available(self) -> bool:
		"""Whether the user may view in video-only mode"""
		return self.view_button == self.ButtonState.ENABLED

	@property
	def shared_available(self) -> bool:
		"""Whether the user may view in shared mode"""
		return self.shared_button == self.ButtonState.ENABLED
	
	@property
	def control_available(self) -> bool:
		"""Whether the user may view in video-only mode"""
		return self.control_button == self.ButtonState.ENABLED
	
	@property
	def exclusive_available(self) -> bool:
		"""Whether the user may view in video-only mode"""
		return self.exclusive_button == self.ButtonState.ENABLED

	"""
	TODO: Additional values not documented

	Additional channel output values in version 4:
	- c_video1 (device ID)
	- c_video1_head (1|2)
	- c_video2 (device ID)
	- c_video2_head (1|2)
	- c_audio (device ID)
	- c_usb (device ID)
	- c_serial (device ID)

	Additional channel output values in version 8:
	- c_usb1 (device ID)
	- c_audio1 (device ID)
	- c_audio2 (device ID)
	- c_sensitive
	- c_rdp_id (RDP ID) only for RDP devices.
	"""


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
	
