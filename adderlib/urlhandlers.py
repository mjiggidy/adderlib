import abc, urllib.parse
import requests
import xmltodict

#class InvalidServerAddressError(RuntimeError):
#	"""The server address provided is missing or invalid"""

class UrlHandler(abc.ABC):
	"""Abstract URL Handler"""

	@abc.abstractclassmethod
	def api_call(cls, server_address:urllib.parse.ParseResult, args:dict) -> dict:
		"""
		Handle a call to the REST API and return a dictionary result
		Data from the Adder API is returned as an XML document and should be returned as a dictionary
		_parse_response() is provided as a good-enough method via xmltodict, but can be overloaded if desired
		"""
		pass

	@classmethod
	def _parse_response(cls, data:str) -> xmltodict.OrderedDict:
		"""Parse an API response to a Python data structure"""
		return xmltodict.parse(data).get("api_response")

	@classmethod
	def _build_url(cls, server_address:urllib.parse.ParseResult, args:dict) -> str:
		"""Build a full URL for an API request"""
		return urllib.parse.urljoin(server_address.geturl(), f"/api/?{urllib.parse.urlencode(args)}")

class RequestsHandler(UrlHandler):
	"""Request handler using the `requests` library"""

	timeout:int=5

	@classmethod
	def api_call(cls, server_address:urllib.parse.ParseResult, args:dict) -> xmltodict.OrderedDict:
		"""GET a call to the API"""

		response = requests.get(cls._build_url(server_address, args), timeout=cls.timeout)
		
		if not response.ok:
			raise Exception(f"Error contacting {server_address.netloc}: Returned {response.status_code}")

		return cls._parse_response(response.content)


class DebugHandler(UrlHandler):
	"""URL handler for debugging with sample XMLs from the documentation"""
	
	@classmethod
	def api_call(cls, server_address:urllib.parse.ParseResult, args:dict) -> xmltodict.OrderedDict:
		"""Load sample XML return data for the given query"""

		full_url = cls._build_url(server_address, args)
		print(f"Requesting: {full_url}")
		print(f"With params: {args}")
		
		method = args.get("method")[0]

		if method == "login":
			if args.get("password")[0] == "goodpwd":
				with open("example_xml/login.xml") as api_response:
					response = cls._parse_response(api_response.read())
				return response
			else:
				with open("example_xml/login_fail.xml") as api_response:
					response = cls._parse_response(api_response.read())
				return response
		
		if method == "logout":
			with open("example_xml/logout.xml") as api_response:
				response = cls._parse_response(api_response.read())
			return response
		
		elif method == "get_devices":
			with open("example_xml/get_devices.xml") as api_response:
				response = cls._parse_response(api_response.read())
			#	print("Responding with",response)
			return response
		
		elif method == "get_channels":
			with open("example_xml/get_channels.xml") as api_response:
				response = cls._parse_response(api_response.read())
			#	print("Responding with",response)
			return response