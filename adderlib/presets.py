import enum, dataclasses
from .devices import AdderReceiver
from .channels import AdderChannel

class AdderPreset:
	"""Adderlink Preset"""

	@dataclasses.dataclass
	class Pair:
		"""A channel/receiver pair"""
		channel:  AdderChannel
		receiver: AdderReceiver

	@enum.unique
	class ActiveState(enum.Enum):
		FULL    = "full"
		PARTIAL = "partial"
		NONE    = "none"
		UNKNOWN = "unknown"

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
		"""Preset ID"""
		return self._extended.get("cp_id","")
	
	@property
	def name(self) -> str:
		"""Preset name"""
		return self._extended.get("cp_name","")
	
	@property
	def description(self) -> str:
		"""Preset description"""
		return self._extended.get("cp_description","")
	
	@property
	def pair_count(self) -> int:
		"""Number of valid channel/receiver pairs"""
		cp_pairs = self._extended.get("cp_pairs","")
		return int(cp_pairs) if cp_pairs.isnumeric() else 0
	
	@property
	def pair_problem_count(self) -> int:
		"""Number of problematic channel/receiver pairs"""
		problem_cp_pairs = self._extended.get("problem_cp_pairs","0")
		return int(problem_cp_pairs) if problem_cp_pairs.isnumeric() else 0
	
	@property
	def currently_active(self) -> ActiveState:
		"""Determines if any of the channel/receiver pairs are currently active"""
		try:
			return self.ActiveState(self._extended.get("cp_active",""))
		except ValueError:
			return self.ActiveState.UNKNOWN

	@property
	def connected_rx_count(self) -> int:
		"""The number of receivers already connected to this preset"""
		rx_count = self._extended.get("connected_rx_count","")
		return int(rx_count) if rx_count.isnumeric() else 0

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