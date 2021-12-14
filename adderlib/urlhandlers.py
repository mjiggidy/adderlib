import abc, urllib.parse, typing
import requests
import xmltodict

class InvalidServerAddressError(RuntimeError):
	"""The server address provided is missing or invalid"""

class UrlHandler(abc.ABC):
	"""Abstract URL Handler"""

	@abc.abstractmethod
	def api_call(self, rel_url:str) -> dict:
		"""
		Handle a call to the REST API and return a dictionary result
		Data from the Adder API is returned as an XML document and should be returned as a dictionary
		_parse_response() is provided as a good-enough method via xmltodict, but can be overloaded if desired
		"""
		pass

	def _parse_response(self, data:str) -> xmltodict.OrderedDict:
		"""Parse an API response to a Python data structure"""
		return xmltodict.parse(data).get("api_response")

class RequestsHandler(UrlHandler):

	def __init__(self, server_address:typing.Optional[str]=None):
		"""UrlHandler using the Requests module"""
		super().__init__()
		self._server_address = None
		if server_address:
			self.setServerAddress(server_address)
	
	def api_call(self, url:str) -> xmltodict.OrderedDict:
		"""GET a call to the API"""
		if not self._server:
			raise InvalidServerAddressError("Server address is not set")

		response = requests.get(self._abs_url(url))
		
		if not response.ok:
			raise Exception(f"Error contacting {url}: Returned {response.status_code}")

		return self._parse_response(response.content)
	
	def _abs_url(self, rel_url:str) -> str:
		"""Return the absolute URL for an API call"""
		# TODO: Do better
		return f"http://{self._server}/{rel_url}"
	
	def setServerAddress(self, address:str):
		"""
		Set the server address and optional port
		Example: host_name:80
		"""
		self._server = str(address)
	
	@property
	def server_address(self) -> str:
		"""Get the server address"""
		return self._server

class DebugHandler(UrlHandler):
	"""URL handler for debugging with sample XMLs from the documentation"""
	
	def api_call(self, rel_url:str) -> xmltodict.OrderedDict:
		"""Load sample XML return data for the given query"""

		params = urllib.parse.parse_qs(rel_url)
		print(f"Requesting: {rel_url}")
		print(f"With params: {params}")
		
		method = params.get("method")[0]

		if method == "login":
			if params.get("password")[0] == "goodpwd":
				with open("example_xml/login.xml") as api_response:
					response = self._parse_response(api_response.read())
				return response
			else:
				with open("example_xml/login_fail.xml") as api_response:
					response = self._parse_response(api_response.read())
				return response
		
		if method == "logout":
			with open("example_xml/logout.xml") as api_response:
				response = self._parse_response(api_response.read())
			return response
		
		elif method == "get_devices":
			with open("example_xml/get_devices.xml") as api_response:
				response = self._parse_response(api_response.read())
			#	print("Responding with",response)
			return response
		
		elif method == "get_channels":
			with open("example_xml/get_channels.xml") as api_response:
				response = self._parse_response(api_response.read())
			#	print("Responding with",response)
			return response