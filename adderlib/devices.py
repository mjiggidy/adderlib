import enum, abc
from datetime import datetime
from dataclasses import dataclass


class AdderDevice(abc.ABC):
	"""Abstract Adder device"""
	@enum.unique
	class DeviceType(enum.Enum):
		"""Types of Adder devices"""
		RX = 0
		TX = 1
	
	@enum.unique
	class DeviceStatus(enum.Enum):
		"""Operational status of Adder device"""
		UNKNOWN         = -1
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