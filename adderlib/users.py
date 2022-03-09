class AdderUser:
	"""Adder user account"""

	def __init__(self):
		self._username = ""
		self._token = ""
	
	def set_logged_in(self, user:str, token:str):
		"""Log a user in with a valid session token"""
		self._username = user
		self._token = token
	
	def set_logged_out(self):
		"""Log the user out"""
		self._username = ""
		self._token = ""

	@property
	def logged_in(self) -> bool:
		"""Whether the user has been successfully authenticated"""
		return self._username and self._token
	
	@property
	def logged_out(self) -> bool:
		"""Whether the use is not logged in"""
		return not self.logged_in
	
	@property
	def username(self) -> str:
		"""The username for this user"""
		return self._username
	
	@property
	def token(self) -> str:
		"""The authentication token for the current session"""
		return self._token