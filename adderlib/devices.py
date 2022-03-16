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
		# Do a lil copy
		self._extended = {key: val for key,val in properties.items()}
	
	# Human-friendly descriptions
	@property
	def name(self) -> str:
		"""Device name"""
		return self._extended.get("d_name","")

	@property
	def description(self) -> str:
		"""Device description"""
		return self._extended.get("d_description","")

	@property
	def location(self) -> str:
		"""Device location"""
		return self._extended.get("d_location","")
	
	@property
	def date_dadded(self) -> datetime:
		"""The date/time this device was set up"""
		return datetime.fromisoformat(self._extended.get("d_date_added"))
	
	# Addresses and IDs
	@property
	def id(self) -> str:
		"""Device ID"""
		return self._extended.get("d_id","")
	
	@property
	def serial_number(self) -> str:
		"""Device serial number"""
		return self._extended.get("d_serial_number","")
	
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
	def mac_addresses(self) -> typing.Tuple[str]:
		"""MAC addresses of the interfaces"""
		return (self._extended.get("d_mac_address",""), self._extended.get("d_mac_address2",""))
	
	@property
	def mac_address(self) -> str:
		"""Primary MAC address"""
		return self.mac_addresses[0]

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
		return self._extended.get("d_firmware","")
	
	@property
	def backup_firmware(self) -> str:
		"""Backup firmware version"""
		return self._extended.get("d_backup_firmware","")
	
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
			if self._extended.get("d_version") == '2':
				return self.DeviceModel(self._extended.get("d_variant"))
			else:
				return self.DeviceModel(self._extended.get("d_version"))
		except:
			return self.DeviceModel.UNKNOWN

	def __repr__(self):
		return f"<{self.__class__.__name__} name=\"{self.name}\" location=\"{self.location}\" model={self.model.name} id={self.id}>"


class AdderTransmitter(AdderDevice):
	"""Adderlink Transmitter (TX) Device"""

	@property
	def channel_count(self) -> int:
		"""Number of channels that use this device"""
		return int(self._extended.get("count_transmitter_channels",0))
	
	@property
	def preset_count(self) -> int:
		"""Number of presets that use this device"""
		return int(self._extended.get("count_transmitter_presets",0))


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
		if self._extended.get("con_start_time"):
			return datetime.fromisoformat(self._extended.get("con_start_time"))
		else:
			return None
		
	@property
	def connection_end(self) -> typing.Optional[datetime]:
		"""Time the last known connection was ended.  Returns None if connection is current."""
		if self._extended.get("con_end_time"):
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
		return self._extended.get("c_name","")

	@property
	def is_connected(self) -> bool:
		"""Is the receiver currently connected to a channel"""
		return self.connection_start and not self.connection_end
	
	# Connected user info
	@property
	def last_username(self) -> str:
		"""Last known username"""
		return self._extended.get("u_username","")
	
	@property
	def last_userid(self) -> str:
		"""Last known user ID"""
		print(self._extended)
		return self._extended.get("u_id","")
	
	@property
	def current_username(self) -> str:
		"""Name of current user connected"""
		return self.last_username if self.is_connected else ""

	@property
	def current_userid(self) -> str:
		"""User ID of current user connected"""
		return self.last_userid if self.is_connected else ""
	
	# Stats
	@property
	def group_count(self) -> int:
		"""Number of receiver groups this belongs to"""
		return int(self._extended.get("count_receiver_groups",0))

	@property
	def preset_count(self) -> int:
		"""Number of receiver presets this belongs to"""
		return int(self._extended.get("count_receiver_presets",0))
	
	@property
	def user_count(self) -> int:
		"""Number of users with access to this receiver"""
		return int(self._extended.get("count_users",0)) 

class AdderUSBExtender(abc.ABC):
	"""Abstract Adder C-USB LAN Extender Device"""
	
	def __init__(self, properties:dict):
		# Do a lil copy
		self._extended = {key: val for key,val in properties.items()}
	
	@property
	def name(self) -> str:
		"""Device name"""
		return self._extended.get("d_name","")
	
	@property
	def ip_address(self) -> typing.Union[ipaddress.IPv4Address, ipaddress.IPv6Address, None]:
		return ipaddress.ip_address(self._extended.get("ip")) if self._extended.get("ip") else None

	@property
	def mac_address(self) -> str:
		return self._extended.get("mac","")
	
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
		return self._extended.get("connectedTo","")

class AdderServer:
	"""An Adder Server Device"""

	@enum.unique
	class Role(enum.Enum):
		"""The role of the AIM"""
		SOLO    = "solo",
		BACKUP  = "backup",
		PRIMARY = "primary",
		UNCONFIGURED = "unconfigured",
		UNKNOWN = "unknown"
	
	@enum.unique
	class Status(enum.Enum):
		"""The status of the AIM"""
		ACTIVE   = "active",
		STANDBY  = "standby",
		FAILED   = "failed",
		QUISCENT =  "quiscent",
		UNKNOWN  = "unknown"
	
	@enum.unique
	class DualEthernetConfig(enum.Enum):
		"""The configuration of the second ethernet port"""
		NO      = 0,
		DHCP    = 1,
		STATIC  = 2,
		BONDED  = 3,
		UNKNOWN = -1


	def __init__(self, properties:dict):
		# Do a lil copy
		self._extended = {key: val for key,val in properties.items()}
	
	# Human-friendly descriptions
	@property
	def name(self) -> str:
		"""Server name"""
		return self._extended.get("name","")

	@property
	def description(self) -> str:
		"""Server description"""
		return self._extended.get("description","")

	@property
	def location(self) -> str:
		"""Server location"""
		return self._extended.get("location","")
	
	@property
	def role(self) -> Role:
		"""The configured role of the AIM"""
		try:
			return self.Role(self._extended.get("role"))
		except Exception:
			return self.Role("unknown")
	
	@property
	def status(self) -> Status:
		"""The current status of the AIM"""
		try:
			return self.Status(self._extended.get("status"))
		except Exception:
			return self.Status("unknown")
	
	@property
	def ip_addresses(self) -> typing.Tuple[typing.Union[ipaddress.IPv4Address,ipaddress.IPv6Address,None]]:
		"""IP addresses on the network"""
		return (
			ipaddress.ip_address(self._extended.get("ip")) if self._extended.get("ip") else None,
			ipaddress.ip_address(self._extended.get("ip2")) if self._extended.get("ip2") else None,
		)
	
	@property
	def ip_address(self) -> typing.Union[ipaddress.IPv4Address,ipaddress.IPv6Address,None]:
		"""Primary IP address of the device"""
		return self.ip_addresses[0] or None

	@property
	def mac_addresses(self) -> typing.Tuple[str]:
		"""MAC addresses of the interfaces"""
		return (self._extended.get("mac",""), self._extended.get("mac2",""))
	
	@property
	def mac_address(self) -> str:
		"""Primary MAC address"""
		return self.mac_addresses[0]

	@property
	def dual_ethernet_config(self) -> DualEthernetConfig:
		"""The configuration of the second ethernet port"""
		try:
			return self.DualEthernetConfig(int(self._extended.get("eth1",-1)))
		except Exception:
			return self.DualEthernetConfig(-1)