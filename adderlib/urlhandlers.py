import abc, urllib.parse
import xmltodict


class UrlHandler(abc.ABC):
	"""Abstract URL Handler"""

	@classmethod
	@abc.abstractmethod
	def api_call(url) -> dict:
		"""Handle a call to the REST API and return a dictionary result"""
		pass


class DebugHandler(UrlHandler):
	
	"""URL handler for debugging with sample XMLs from the documentation"""
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