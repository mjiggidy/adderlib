import abc, pathlib, urllib.parse
import requests, xmltodict

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
	"""
	URL handler for debugging with sample XMLs from the documentation
	Class properties:
		dirpath:str  -- A path to the directory containing the sample XML responses (default: ./example_xml)
		verbose:bool -- Flag to print debug data to stdout (default: False)
	"""

	dirpath: pathlib.Path = "./example_xml"
	verbose: bool = False

	@classmethod
	def api_call(cls, server_address:urllib.parse.ParseResult, args:dict) -> xmltodict.OrderedDict:
		"""Load sample XML return data for the given query"""

		full_url = cls._build_url(server_address, args)
					
		method = args.get("method")
		if not method:
			raise Exception("Invalid API call: No method specified.")

		path_response = pathlib.Path(cls.dirpath, method).with_suffix(".xml")

		if cls.verbose:
			print(f"Requesting:     {full_url}")
			print(f"With params:    {args}")
			print(f"Method given:   {method}")
			print(f"Using response: {path_response}")	

		if not path_response.is_file():
			raise FileNotFoundError(f"No example XML found for method '{method}' in {cls.dirpath}")

		with path_response.open('r') as file_response:
			return cls._parse_response(file_response.read())