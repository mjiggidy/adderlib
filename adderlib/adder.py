import urllib.parse, typing

from .urlhandlers import UrlHandler, RequestsHandler
from .users import AdderUser
from .devices import AdderDevice, AdderReceiver, AdderTransmitter, AdderServer, AdderUSBExtender, AdderUSBReceiver, AdderUSBTransmitter
from .channels import AdderChannel
from .presets import AdderPreset

class AdderRequestError(Exception):
	"""Adder API request has not returned success"""
	pass

class AdderAPI:

	def __init__(self,server_address:str,*,url_handler:typing.Optional[UrlHandler]=None, user:typing.Optional[AdderUser]=None, api_version:typing.Optional[int]=8):
		"""Adderlink API for interacting with devices, channels, and users"""

		self._setServerAddress(server_address)
		self.setUrlHandler(url_handler or RequestsHandler())
		self.setUser(user or AdderUser())
		self.setApiVersion(api_version)
	
	def _setServerAddress(self, server_address:str):
		"""Set the server address to use"""

		# If no schema defined, indicate that properly in the address
		if "//" not in server_address:
			server_address = "//" + server_address
		
		self._server_address = urllib.parse.urlparse(server_address, scheme="http")

	def setUrlHandler(self, handler:UrlHandler):
		"""Set the UrlHandler to use for AdderAPI URL calls"""
		if not isinstance(handler, UrlHandler):
			raise ValueError(f"URL handler {type(handler)} is not an instance of UrlHandler")
		self._url_handler = handler

	def setUser(self, user:AdderUser):
		"""Set the AdderUser to use for AdderAPI calls"""
		if not isinstance(user, AdderUser):
			raise ValueError(f"User type{type(user)} is not an instance of AdderUser")
		self._user = user

	def setApiVersion(self, version:int):
		"""Set the API version to use"""
		self._api_version = int(version)

	# User authentication
	def login(self, username:str, password:str):
		"""Log the user in to the KVM system and retrieve an API token"""
		
		args = {
			"v":self._api_version,
			"method":"login",
			"username":username,
			"password":password
		}

		response = self._url_handler.api_call(self._server_address, args)
		
		if response.get("success") == "1" and response.get("token") is not None:
			self._user.set_logged_in(username, response.get("token"))
		
		elif "errors" in response:
			error = response.get("errors").get("error")
			raise AdderRequestError(f"Error {error.get('code','?')}: {error.get('msg','?')}")
		
		else:
			raise Exception("Unknown error")
	
	def logout(self):
		"""Log the user out"""

		args = {
			"v":self._api_version,
			"method":"logout",
			"token":self._user.token
		}

		response = self._url_handler.api_call(self._server_address, args)

		# TODO: More detailed error handling?
		# TODO: Maybe have the URL handler throw an exception?
		if response.get("success") == "1":
			self._user.set_logged_out()
		else:
			raise AdderRequestError()
		
	# Device management
	def getTransmitters(self, t_id:typing.Optional[str]=None) -> typing.Generator[AdderTransmitter, None, None]:
		"""Request a list of available Adderlink transmitters"""

		args = {
			"v":self._api_version,
			"token":self._user.token,
			"method":"get_devices",
			"device_type":"tx"
		}

		response = self._url_handler.api_call(self._server_address, args)

		if response.get("success") == "1" and "devices" in response:

			# It seems `xmltodict` only returns a list of nodes if there are more than one
			if response.get("count_devices") == "1":
				transmitters_list = [response.get("devices").get("device")]
			else:
				transmitters_list = response.get("devices").get("device")


			for device in transmitters_list:
				tx = AdderTransmitter(device)
				# Quick n dirty filtering since API does not support it natively
				if t_id is not None and t_id != tx.id:
					continue
				yield tx
			
	def getReceivers(self, r_id:typing.Optional[str]=None) -> typing.Generator[AdderReceiver, None, None]:
		"""Request a list of available Adderlink receivers"""

		args = {
			"v":self._api_version,
			"token":self._user.token,
			"method":"get_devices",
			"device_type":"rx"
		}

		response = self._url_handler.api_call(self._server_address, args)

		if response.get("success") == "1" and "devices" in response:

			# It seems `xmltodict` only returns a list of nodes if there are more than one
			if response.get("count_devices") == "1":
				receivers_list = [response.get("devices").get("device")]
			else:
				receivers_list = response.get("devices").get("device")

			for device in receivers_list:
				rx = AdderReceiver(device)
				# Quick n dirty filtering since API does not support it natively
				if r_id is not None and r_id != rx.id:
					continue
				yield rx

	# Device management
	def getServers(self) -> typing.Generator[AdderServer, None, None]:
		"""Request a list of available Adderlink AIM Servers"""

		args = {
			"v":self._api_version,
			"token":self._user.token,
			"method":"get_servers"
		}

		response = self._url_handler.api_call(self._server_address, args)

		if response.get("success") == "1" and "servers" in response:

			# It seems `xmltodict` only returns a list of nodes if there are more than one
			if response.get("count_servers") == "1":
				servers_list = [response.get("servers").get("server")]
			else:
				servers_list = response.get("servers").get("server")

			for server in servers_list:
				yield AdderServer(server)
	
	def setDeviceInfo(self, device:AdderDevice, *, description:typing.Optional[str]=None, location:typing.Optional[str]=None):
		"""Update the information for an existing device"""

		args = {
			"v": self._api_version,
			"token": self._user.token,
			"method": "update_device",
			"id": device.id
		}

		# Providing neither arguments will cause an API error anyway.  Might as well check here.
		if description is None and location is None:
			raise ValueError("At least one of `description` or `location` must be provided")

		# Set to underscore to properly clear an existing value (passing a blank string won't work)
		if description is not None:
			args.update({"desc": '_' if not len(description.strip()) else description})
		if location is not None:
			args.update({"loc": '_' if not len(location.strip()) else location})

		response = self._url_handler.api_call(self._server_address, args)			
			
		if response.get("success") == "1":
			return
		
		elif "errors" in response:
			error = response.get("errors").get("error")
			raise AdderRequestError(f"Error {error.get('code','?')}: {error.get('msg','?')}")
		
		else:
			raise Exception("Unknown error")
	
	def rebootDevices(self, devices:typing.Union[typing.Iterable[AdderDevice], AdderDevice]):
		"""Reboot one or more devices"""
		
		devices = [devices] if isinstance(devices, AdderDevice) else devices

		args = {
			"v":self._api_version,
			"token":self._user.token,
			"method":"reboot_devices",
			"ids": ','.join(d.id for d in devices)
		}

		response = self._url_handler.api_call(self._server_address, args)

		if response.get("success") == "1":
			return
		
		elif "errors" in response:
			error = response.get("errors").get("error")
			raise AdderRequestError(f"Error {error.get('code','?')}: {error.get('msg','?')}")

	
	# Channel management
	def getChannels(self, id:typing.Optional[str]=None, name:typing.Optional[str]="") -> typing.Generator[AdderChannel, None, None]:
		"""Request a list of available Adderlink channels"""

		args = {
			"v":self._api_version,
			"token":self._user.token,
			"method":"get_channels",
			"filter_c_name": name or ""
		}

		response = self._url_handler.api_call(self._server_address, args)
		
		if response.get("success") == "1" and "channels" in response:

			# It seems `xmltodict` only returns a list of nodes if there are more than one
			if response.get("count_channels") == "1":
				channel_list = [response.get("channels").get("channel")]
			else:
				channel_list = response.get("channels").get("channel")

			for channel in channel_list:
				ch = AdderChannel(channel)
				if id is not None and id != ch.id:
					continue
				yield AdderChannel(channel)
	
	def createChannel(self,
		name:str, description:typing.Optional[str]=None, location:typing.Optional[str]=None, modes:typing.Optional[list[AdderChannel.ConnectionMode]]=None, 
		video1:typing.Optional[AdderTransmitter]=None, video1_head:typing.Optional[int]=None,
		video2:typing.Optional[AdderTransmitter]=None, video2_head:typing.Optional[int]=None,
		audio:typing.Optional[AdderTransmitter]=None, usb:typing.Optional[AdderTransmitter]=None, serial:typing.Optional[AdderTransmitter]=None,
		group_name:typing.Optional[str]=None) -> AdderChannel:
		"""Create a new channel from the specified transmitters"""

		modes = modes or []
		
		args = {
			"v":self._api_version,
			"token":self._user.token,
			"method":"create_channel",
			"name":name,
			"desc":description,
			"loc":location,
			"allowed":str().join([m.value for m in modes]).lower(),
			"groupname":group_name
		}

		# Video 1
		if video1:
			args.update({
				"video1":video1.id,
				"video1head":video1_head
			})
		
		# Video 2
		if video2:
			args.update({
				"video2":video2.id,
				"video2head":video2_head
			})
		
		# Audio
		if audio:
			args.update({"audio":audio.id})
		
		# USB
		if usb:
			args.update({"usb":usb.id})
		
		# Serial
		if serial:
			args.update({"serial":serial.id})
		
		response = self._url_handler.api_call(self._server_address, args)
		if response.get("success") == "1" and response.get("id"):
			return next(self.getChannels(id=response.get("id")))
		
		elif "errors" in response:
			error = response.get("errors").get("error")
			raise AdderRequestError(f"Error {error.get('code','?')}: {error.get('msg','?')}")
		
		else:
			raise Exception("Unknown error")


	def connectToChannel(self, channel:AdderChannel, receiver:AdderReceiver, mode:typing.Optional[AdderChannel.ConnectionMode]=AdderChannel.ConnectionMode.SHARED):
		"""Connect a channel to a receiver"""

		args = {
			"v":self._api_version,
			"token":self._user.token,
			"method":"connect_channel",
			"c_id":channel.id,
			"rx_id":receiver.id,
			"mode":mode.value
		}

		response = self._url_handler.api_call(self._server_address, args)
		if response.get("success") == "1":
			return
		
		elif "errors" in response:
			error = response.get("errors").get("error")
			raise AdderRequestError(f"Error {error.get('code','?')}: {error.get('msg','?')}")
		
		else:
			raise Exception("Unknown error")
		
	def disconnectFromChannel(self, receiver:typing.Union[AdderReceiver, typing.Iterable[AdderReceiver]], force:typing.Optional[bool]=False):
		"""Disconnect a receiver -- or iterable of receivers -- from its current channel"""
		receiver = [receiver] if isinstance(receiver, AdderReceiver) else receiver

		args = {
			"v":self._api_version,
			"token": self._user.token,
			"method":"disconnect_channel",
			"rx_id":','.join(x.id for x in receiver),
			"force":int(force)
		}

		response = self._url_handler.api_call(self._server_address, args)
		
		if response.get("success") == "1":
			return

		elif "errors" in response:
			error = response.get("errors").get("error")
			raise AdderRequestError(f"Error {error.get('code','?')}: {error.get('msg','?')}")

	def deleteChannel(self, channel:AdderChannel):
		"""Delete a channel.  Admin privileges are required."""
		args = {
			"v": self._api_version,
			"token": self._user.token,
			"method": "delete_channel",
			"id": channel.id
		}
		
		response = self._url_handler.api_call(self._server_address, args)

		if response.get("success") == "1":
			return

		elif "errors" in response:
			error = response.get("errors").get("error")
			raise AdderRequestError(f"Error {error.get('code','?')}: {error.get('msg','?')}")		
	
	# Preset management
	def getPresets(self, id:typing.Optional[str]=None) -> typing.Generator[AdderPreset, None, None]:
		"""Request a list of available Adderlink presets"""

		args = {
			"v":self._api_version,
			"token":self._user.token,
			"method":"get_presets"
		}

		response = self._url_handler.api_call(self._server_address, args)
		
		if response.get("success") == "1" and "connection_presets" in response:

			# It seems `xmltodict` only returns a list of nodes if there are more than one
			if response.get("count_presets") == "1":
				presets_list = [response.get("connection_presets").get("connection_preset")]
			else:
				presets_list = response.get("connection_presets").get("connection_preset")

			for preset in presets_list:
				ps = AdderPreset(preset)
				if id is not None and id != ps.id:
					continue
				yield ps
	
	def createPreset(self, name:str, pairs:typing.Union[typing.Iterable[AdderPreset.Pair], AdderPreset.Pair], modes:typing.Union[typing.Iterable[AdderChannel.ConnectionMode], AdderChannel.ConnectionMode]) -> AdderPreset:
		"""Create a preset consisting of one or more channel/receiver pairs"""

		if not len(name.strip()):
			raise ValueError("'name' parameter must not be empty")
		name_formatted = urllib.parse.quote(name)

		if isinstance(pairs, AdderPreset.Pair):
			pairs = [pairs]
		pairs_formatted = ','.join(f"{pair.channel.id}-{pair.receiver.id}" for pair in pairs) # TODO: Handle 'ch.id-rx.id' formatting in Preset __str__?

		if isinstance(modes, AdderChannel.ConnectionMode):
			modes = [modes]
		modes_formatted = str().join(mode.value for mode in modes)

		args = {
			"v":self._api_version,
			"token":self._user.token,
			"method":"create_preset",
			"name":name_formatted,
			"pairs":pairs_formatted,
			"allowed":modes_formatted
		}

		response = self._url_handler.api_call(self._server_address, args)

		if response.get("success") == "1" and response.get("id"):
			return next(self.getPresets(response.get("id")))
		
		elif "errors" in response:
			raise Exception(f"Errors: {response.get('errors')}")
			#for error in response.get("errors").get("error"):
			#	raise Exception(f"Error {error.get('code','?')}: {error.get('msg','?')}")
	
	def loadPreset(self, preset:AdderPreset, mode:AdderChannel.ConnectionMode, force:typing.Optional[bool]=False):
		"""Connect a preset"""

		args = {
			"v":self._api_version,
			"token":self._user.token,
			"method":"connect_preset",
			"id":preset.id,
			"mode":mode.value,
			"force":int(force)
		}

		response = self._url_handler.api_call(self._server_address, args)
		
		if response.get("success") == "1":
			return
		
		elif "errors" in response:
			raise Exception(f"Errors: {response.get('errors')}")
	
	def unloadPreset(self, preset:AdderPreset, force:typing.Optional[bool]=False):
		"""Disconnect a preset"""

		args = {
			"v":self._api_version,
			"token":self._user.token,
			"method":"disconnect_preset",
			"id":preset.id,
			"force":int(force)
		}

		response = self._url_handler.api_call(self._server_address, args)
		
		if response.get("success") == "1":
			return
		
		elif "errors" in response:
			raise Exception(f"Errors: {response.get('errors')}")

	def deletePreset(self, preset:AdderPreset):
		"""Delete a preset"""

		args = {
			"v":self._api_version,
			"token":self._user.token,
			"method":"delete_preset",
			"id":preset.id
		}

		response = self._url_handler.api_call(self._server_address, args)
		
		if response.get("success") == "1":
			return
		
		elif "errors" in response:
			raise Exception(f"Errors: {response.get('errors')}")
	
	# C-USB Lan Extender Management
	def getUSBReceivers(self, mac_address:typing.Optional[AdderUSBReceiver]=None) -> typing.Generator[AdderUSBReceiver, None, None]:
		"""Get a list of C-USB LAN Receivers, optionally filtered by MAC address"""

		args = {
			"v":self._api_version,
			"token":self._user.token,
			"method":"get_all_c_usb"
		}

		response = self._url_handler.api_call(self._server_address, args)

		if response.get("success") == "1" and "c_usb_lan_extenders" in response:

			# It seems `xmltodict` only returns a list of nodes if there are more than one
			if response.get("count_c_usbs") == "1":
				usb_list = [response.get("c_usb_lan_extenders").get("c_usb")]
			else:
				usb_list = response.get("c_usb_lan_extenders").get("c_usb")

			for usb in usb_list:
				if usb.get("type","") != "rx": continue

				rx = AdderUSBReceiver(usb)

				# Quick n dirty filtering since API does not support it natively
				if mac_address is not None and mac_address != rx.mac_address:
					continue

				yield rx

	# C-USB Lan Extender Management
	# TODO: Currently untested
	
	def getUSBTransmitters(self, mac_address:typing.Optional[AdderUSBTransmitter]=None) -> typing.Generator[AdderUSBTransmitter, None, None]:
		"""Get a list of C-USB LAN Transmitters, optionally filtered by MAC address"""

		args = {
			"v":self._api_version,
			"token":self._user.token,
			"method":"get_all_c_usb"
		}

		response = self._url_handler.api_call(self._server_address, args)

		if response.get("success") == "1" and "c_usb_lan_extenders" in response:

			# It seems `xmltodict` only returns a list of nodes if there are more than one
			if response.get("count_c_usbs") == "1":
				usb_list = [response.get("c_usb_lan_extenders").get("c_usb")]
			else:
				usb_list = response.get("c_usb_lan_extenders").get("c_usb")

			for usb in usb_list:
				if usb.get("type","") != "tx": continue

				tx = AdderUSBTransmitter(usb)

				# Quick n dirty filtering since API does not support it natively
				if mac_address is not None and mac_address != tx.mac_address:
					continue

				yield tx
	
	def deleteUSBExtender(self, usb:AdderUSBExtender):
		"""Delete a C-USB LAN Transmitter or Receiver"""

		args = {
			"v":self._api_version,
			"token":self._user.token,
			"method":"delete_c_usb",
			"mac":usb.mac_address
		}

		response = self._url_handler.api_call(self._server_address, args)
		
		if response.get("success") == "1":
			return
		
		elif "errors" in response:
			raise Exception(f"Errors: {response.get('errors')}")
	
	def setUSBExtenderInfo(self, usb:AdderUSBExtender, *, name:str):
		"""Update the information for an existing USB extender"""

		args = {
			"v":self._api_version,
			"token":self._user._token,
			"method":"update_c_usb",
			"mac":usb.mac_address,
			"name":name
		}

		response = self._url_handler.api_call(self._server_address, args)
	
		if response.get("success") == "1":
			return
		
		elif "errors" in response:
			raise Exception(f"Errors: {response.get('errors')}")


	def connectUSBExtender(self, receiver:AdderUSBReceiver, transmitter:AdderUSBTransmitter):
		"""Connect a C-USB LAN Receiver to a Transmitter"""

		args = {
			"v":self._api_version,
			"token":self._user._token,
			"method":"connect_c_usb",
			"rx": receiver.mac_address,
			"tx": transmitter.mac_address
		}

		response = self._url_handler.api_call(self._server_address, args)
	
		if response.get("success") == "1":
			return
		
		elif "errors" in response:
			raise Exception(f"Errors: {response.get('errors')}")

	def disconnectUSBExtender(self, receiver:AdderUSBReceiver):
		"""Connect a C-USB LAN Receiver to a Transmitter"""

		args = {
			"v":self._api_version,
			"token":self._user._token,
			"method":"disconnect_c_usb",
			"mac": receiver.mac_address,
		}

		response = self._url_handler.api_call(self._server_address, args)
	
		if response.get("success") == "1":
			return
		
		elif "errors" in response:
			raise Exception(f"Errors: {response.get('errors')}")
	
	def replaceDevice(self, old_device:AdderDevice, new_device:AdderDevice):
		"""Replace an old device with a new one"""

		args = {
			"v": self._api_version,
			"token": self._user._token,
			"method": "replace_device",
			"d_id": old_device.id,
			"r_d_id": new_device.id
		}

		response = self._url_handler.api_call(self._server_address, args)

		if response.get("success") == "1":
			return
		
		elif "errors" in response:
			raise Exception(f"Errors: {response.get('errors')}")
	
	def identifyDevice(self, device:AdderDevice):
		"""Sends an 'identify' command to the specified device"""

		args = {
			"v": self._api_version,
			"token": self._user._token,
			"method": "identify_device",
			"id": device.id
		}

		response = self._url_handler.api_call(self._server_address, args)

		if response.get("success") == "1":
			return
		
		elif "errors" in response:
			raise Exception(f"Errors: {response.get('errors')}")

	@property
	def user(self) -> AdderUser:
		"""Get the current user"""
		return self._user

	@property
	def server_address(self) -> urllib.parse.ParseResult:
		"""Get the server address"""
		return self._server_address
	
	@property
	def url_handler(self) -> UrlHandler:
		"""Get the URL Handler"""
		return self._url_handler