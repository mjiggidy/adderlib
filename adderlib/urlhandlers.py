import abc, urllib.parse
import requests, requests.compat
import xmltodict

class UrlHandler(abc.ABC):
	"""Abstract URL Handler"""

	@abc.abstractmethod
	def api_call(self, url:str) -> dict:
		"""Handle a call to the REST API and return a dictionary result"""
		pass

	def parse_response(self, data:str) -> xmltodict.OrderedDict:
		"""Parse an API response to a Python data structure"""
		return xmltodict.parse(data).get("api_response")

class RequestsHandler(UrlHandler):

	def __init__(self, address:str="localhost"):
		"""UrlHandler using the Requests module"""
		self.setServerAddress(address)
	
	def api_call(self, url:str) -> xmltodict.OrderedDict:
		"""GET a call to the API"""
		response = requests.get(self._abs_url(url))
		
		if not response.ok:
			raise Exception(f"Error contacting {url}: Returned {response.status_code}")

		return self.parse_response(response.content)
	
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

class DebugHandler(UrlHandler):
	
	"""URL handler for debugging with sample XMLs from the documentation"""
	def api_call(self, url) -> xmltodict.OrderedDict:

		params = urllib.parse.parse_qs(url)
		print(f"Requesting: {url}")
		print(f"With params: {params}")
		
		method = params.get("method")[0]

		if method == "login":
			if params.get("password")[0] == "goodpwd":
				with open("example_xml/login.xml") as api_response:
					response = self.parse_response(api_response.read())
				return response
			else:
				with open("example_xml/login_fail.xml") as api_response:
					response = self.parse_response(api_response.read())
				return response
		
		if method == "logout":
			with open("example_xml/logout.xml") as api_response:
				response = self.parse_response(api_response.read())
			return response
		
		elif method == "get_devices":
			with open("example_xml/get_devices.xml") as api_response:
				response = self.parse_response(api_response.read())
			#	print("Responding with",response)
			return response
		
		elif method == "get_channels":
			with open("example_xml/get_channels.xml") as api_response:
				response = self.parse_response(api_response.read())
			#	print("Responding with",response)
			return response