import enum


class AdderChannel:
	"""Adderlink channel"""

	@enum.unique
	class ConnectionMode(enum.Enum):
		VIEW_ONLY = 'v'
		SHARED    = 's'
		EXCLUSIVE = 'e'
		PRIVATE   = 'p'

	@enum.unique
	class ButtonState(enum.Enum):
		"""Video-only mode capabilities"""
		UNKNOWN  = "unknown"  # Unknown state
		DISABLED = "disabled" # Disabled because in use
		ENABLED  = "enabled"  # Enabled
		HIDDEN   = "hidden"   # Never allowed

	def __init__(self, properties:dict):
		self._extended = {key: val for key,val in properties.items()}
	
	@property
	def id(self) -> str:
		"""Channel ID"""
		return self._extended.get("c_id","")
	
	@property
	def name(self) -> str:
		"""Channel name"""
		return self._extended.get("c_name","")
	
	@property
	def description(self) -> str:
		"""Channel description"""
		return self._extended.get("c_description","")
	
	@property
	def location(self) -> str:
		"""Channel location"""
		return self._extended.get("c_location","")
	
	@property
	def type(self) -> str:
		"""Channel type"""
		# TODO: Investigate.  Not in the documentation
		return self._extended.get("c_channel_type","")

	@property
	def tx_id(self) -> str:
		"""Device ID"""
		# TODO: Investigate.  Not in the documentation
		return self._extended.get("c_tx_id","")
	
	@property
	def is_online(self) -> bool:
		"""Device status"""
		# TODO: Investigate.  Not in the documentation
		return self._extended.get("channel_online") == "1"
	
	@property
	def is_favorite(self) -> bool:
		"""Whether the channel has been favorited"""
		return self._extended.get("c_favourite") != "false"
	
	@property
	def shortcut(self) -> str:
		"""Returns the shortcut index if set"""
		return self._extended.get("c_favourite","") if self.is_favorite else ''
	
	@property
	def view_button(self) -> ButtonState:
		"""Indicates the state of the video-only view button"""
		state = self._extended.get("view_button")
		try:
			return self.ButtonState(state)
		except ValueError:
			return self.ButtonState.UNKNOWN
	
	@property
	def shared_button(self) -> ButtonState:
		"""Indicates the state of the shared view button"""
		state = self._extended.get("shared_button")
		try:
			return self.ButtonState(state)
		except ValueError:
			return self.ButtonState.UNKNOWN

	@property
	def control_button(self) -> ButtonState:
		"""Indicates the state of the full-control button"""
		state = self._extended.get("control_button")
		try:
			return self.ButtonState(state)
		except ValueError:
			return self.ButtonState.UNKNOWN

	@property
	def exclusive_button(self) -> ButtonState:
		"""Indicates the state of the video-only view button"""
		state = self._extended.get("exclusive_button")
		try:
			return self.ButtonState(state)
		except ValueError:
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
	
	
	def _print_undocumented(self):
		"""Undocumented features"""
		for property in ["c_video1","c_video1_head","c_video2","c_video2_head","c_audio","c_usb","c_serial","c_usb1", "c_audio1","c_audio2","c_sensitive","c_rdp_id"]:
			print(f"{property.ljust(16)}: {self._extended.get(property,'Not Set')}")
		


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

	def __repr__(self):
		return f"<{self.__class__.__name__} name=\"{self.name}\" is_online={self.is_online} id={self.id}>"