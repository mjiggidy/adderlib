import enum, abc, ipaddress, typing
from datetime import datetime
from dataclasses import dataclass

@dataclass
class NetworkInterface:
	"""Network interface info"""
	ip_address:typing.Union[ipaddress.IPv4Address,ipaddress.IPv6Address]
	mac_address:str
	is_online:bool


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
		UNKNOWN  =  '?'
		ALIF1000 =  '1'
		ALIF2002 =  'b'
		ALIF2112 =  'v'
		ALIF1002 =  's'
		ALIF2020 =  't'
		ALIF100T =  'd'
		ALIF100T_VGA = 'f',
		ALIF101T_HDMI = 'h',
		ALIF4021R = '4',
		ALIFE300R = '8'
	
	
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
	def ip_addresses(self) -> typing.Tuple[typing.Union[ipaddress.IPv4Address,ipaddress.IPv6Address,None]]:
		"""IP addresses on the network"""
		return (
			ipaddress.ip_address(self._extended.get("d_ip_address")) if self._extended.get("d_ip_address") else None,
			ipaddress.ip_address(self._extended.get("d_ip_address2")) if self._extended.get("d_ip_address2") else None,
		)
	
	@property
	def ip_address(self) -> typing.Union[ipaddress.IPv4Address,ipaddress.IPv6Address,None]:
		"""Primary IP address of the device"""
		return self.ip_addresses[0] or None

	@property
	def mac_addresses(self) -> typing.Tuple[typing.Union[str,None]]:
		"""MAC addresses of the interfaces"""
		return (self._extended.get("d_mac_address") or None, self._extended.get("d_mac_address2") or None)
	
	@property
	def mac_address(self) -> str:
		"""Primary MAC address"""
		return self.mac_addresses[0] or None

	@property
	def network_interfaces(self) -> typing.Tuple[NetworkInterface]:
		"""Return network interfaces"""
		return (
			NetworkInterface(self.ip_addresses[0], self.mac_addresses[0], int(self._extended.get("d_online",-1))>0),
			NetworkInterface(self.ip_addresses[1], self.mac_addresses[1], int(self._extended.get("d_online2",-1))>0)
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
		try:
			if self._extended.get("d_version") == '1':
				return self.DeviceModel.ALIF1000
			else:
				return self.DeviceModel(self._extended.get("d_variant"))
		except:
			# print(self._extended.get("d_version"), self._extended.get("d_variant"))
			return self.DeviceModel.UNKNOWN

	def __repr__(self):
		return f"<{self.__class__.__name__} name=\"{self.name}\" location=\"{self.location}\" model={self.model} id={self.id}>"


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
	
	# Connection info

	@property
	def connection_start(self) -> typing.Optional[datetime]:
		"""Time the last known connection started"""
		if self._extended.get("con_start_time") is not None:
			return datetime.fromisoformat(self._extended.get("con_start_time"))
		else:
			return None
		
	@property
	def connection_end(self) -> typing.Optional[datetime]:
		"""Time the last known connection was ended.  Returns None if connection is current."""
		if self._extended.get("con_end_time") is not None:
			return datetime.fromisoformat(self._extended.get("con_end_time"))
		else:
			return None

	@property
	def connection_control(self) -> ConnectionControlType:
		"""Control mode of the last known connection"""
		con_type = int(self._extended.get("con_control", -1))
		try:
			return self.ConnectionControlType(con_type)
		except Exception:
			return self.ConnectionControlType(-1)
	
	@property
	def channel_name(self) -> str:
		"""The name of the last known channel this receiver was connected"""
		return self._extended.get("c_name")

	@property
	def is_connected(self) -> bool:
		"""Is the receiver currently connected to a channel"""
		return self.connection_start and not self.connection_end
	
	# Connected user info
	@property
	def last_username(self) -> typing.Optional[str]:
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

class AdderUSBExtender(abc.ABC):
	"""Abstract Adder C-USB LAN Extender Device"""

	@enum.unique
	class DeviceType(enum.Enum):
		"""Types of Adder C-USB Lan Extenders"""
		RX = 0
		TX = 1
	
	def __init__(self, properties:dict):
		self._extended = {key: val for key,val in properties.items()}
	
	@abc.abstractproperty
	def device_type(self) -> DeviceType:
		"""Type of Adder device"""
		pass
	
	@property
	def name(self) -> str:
		"""Device name"""
		return self._extended.get("d_name") or None
	
	@property
	def ip_address(self) -> typing.Union[ipaddress.IPv4Address, ipaddress.IPv6Address]:
		return ipaddress.ip_address(self._extended.get("ip")) if self._extended.get("ip") else None

	@property
	def mac_address(self) -> str:
		return self._extended.get("mac")
	
	@property
	def is_online(self) -> bool:
		return self._extended.get("online") == 1
	
	@property
	def network_interface(self) -> NetworkInterface:
		return NetworkInterface(self.ip_address, self.mac_address, self.is_online)

class AdderUSBTransmitter(AdderUSBExtender):
	"""Adder C-USB LAN Network Transmitter"""

class AdderUSBReceiver(AdderUSBExtender):
	"""Adder C-USB Lan Network Receiver"""

	@property
	def connected_to(self) -> str:
		"""MAC address of the connected transmitter"""
		return self._extended.get("connectedTo")