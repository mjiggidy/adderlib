import abc, urllib.parse
import xmltodict

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
		
	
	
