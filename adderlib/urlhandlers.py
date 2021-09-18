import abc, urllib.parse
import requests, requests.compat
import xmltodict

class UrlHandler(abc.ABC):
	"""Abstract URL Handler"""

	@classmethod
	@abc.abstractmethod
	def api_call(url:str) -> dict:
		"""Handle a call to the REST API and return a dictionary result"""
		pass

class RequestsHandler(UrlHandler):

	def __init__(self, address:str, port:int=80):
		self._server = str(address)
		self._port = int(port)
	
	def api_call(self, url:str) -> xmltodict.OrderedDict:
		"""GET a call to the API"""
		response = requests.get(self._abs_url(url))
		
		if not response.ok:
			raise Exception(f"Error contacting {url}: Returned {response.status_code}")

		return xmltodict.parse(response.content).get("api_response")
	
	def _abs_url(self, rel_url:str) -> str:
		"""Return the absolute URL for an API call"""
		# TODO: Do better
		return f"http://{self._server}:{self._port}/{rel_url}"

class DebugHandler(UrlHandler):
	
	"""URL handler for debugging with sample XMLs from the documentation"""
	@classmethod
	def api_call(cls, url) -> xmltodict.OrderedDict:

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
		
		if method == "logout":
			with open("example_xml/logout.xml") as api_response:
				response = xmltodict.parse(api_response.read()).get("api_response")
			return response
		
		elif method == "get_devices":
			with open("example_xml/get_devices.xml") as api_response:
				response = xmltodict.parse(api_response.read()).get("api_response")
			#	print("Responding with",response)
			return response
		
		elif method == "get_channels":
			with open("example_xml/get_channels.xml") as api_response:
				response = xmltodict.parse(api_response.read()).get("api_response")
			#	print("Responding with",response)
			return response

"""
class RequestsHandler(UrlHandler):
	
	import requests

	@classmethod
	def api_call(url) -> dict:
		response = requests.get(url)
		if response.ok:
			return response.content
"""