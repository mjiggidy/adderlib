import abc, urllib.parse

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
		print(f"Requesting: {url}")
		return {"success":1}


class AdderUser:
	"""Authenticated user"""

	def __init__(self):
		self._logged_in = False
		self._username = None
		self._token = None
	
	def set_logged_in(self, user:str, token:str):
		self._username = user
		self._logged_in = True
		self._token = token

	@property
	def logged_in(self) -> bool:
		return self._logged_in
	
	@property
	def username(self) -> str:
		return self._username
	
	@property
	def token(self) -> str:
		return self._token

class AdderAPI:

	def __init__(self, user:AdderUser, url_handler:UrlHandler, api_version:int=8):
		self._user = user
		self._url_handler = url_handler
		self._api_version = api_version

	def login(self, username:str, password:str):
		# TODO: Sanitize inputs
		url = f"/api/?v={self._api_version}&method=login&username={urllib.parse.quote(username)}&password={urllib.parse.quote(password)}"
		response = self._url_handler.api_call(url)

		if response.get("success"):
			self._user.set_logged_in(username, "faketoken")
		
		print(self._user.logged_in)
		print(self._user.token)