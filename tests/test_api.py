import unittest
from adderlib import adder, urlhandlers, channels, devices, presets

# Config
test_user    = "valid_username"				# Provide a valild username if using a live server
test_pass    = "valid_password"				# Provide a valid password if using a live server
test_addr    = "localhost"
test_handler = urlhandlers.DebugHandler()	 # Use DebugHandler for example XML responses
#test_handler= urlhandlers.RequestsHandler() # Use RequestsHandler for live testing with a real server

class TestAuthentication(unittest.TestCase):

	def test_valid_login_cycle(self):
		"""Test a valid user can log in and out"""

		api = adder.AdderAPI(test_addr, url_handler=test_handler)
		self.assertFalse(api.user.logged_in)

		api.login(test_user, test_pass)
		self.assertTrue(api.user.logged_in)

		with self.assertRaises(adder.AdderRequestError):
			api.login(username=test_user, password=test_pass)
		
		api.logout()
		self.assertFalse(api.user.logged_in)

class TestGetters(unittest.TestCase):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.api = adder.AdderAPI(test_addr, url_handler=test_handler)
		self.api.login(username=test_user, password=test_pass)		
	
	def test_valid_channels(self):
		"""Any channels should be returned as AdderChannel objects"""

		# We will have to assume there are channels...
		chans = list(self.api.getChannels())
		self.assertGreater(len(chans), 0)

		for ch in chans:
			self.assertIsInstance(ch, channels.AdderChannel)

	def test_valid_transmitters(self):
		"""Any transmitters should be returned as AdderDevice objects"""
		# Note: DebugHandler does not discriminate between AdderReceiver and AdderTransmitter
		# So checking for parent class AdderDevice
		# If using on a live server, feel free to check for AdderTransmitter

		# We will have to assume there are transmitters...
		trans = list(self.api.getTransmitters())
		self.assertGreater(len(trans), 0)
		
		for tx in trans:
			self.assertIsInstance(tx, devices.AdderDevice)

	def test_valid_receivers(self):
		"""Any receivers should be returned as AdderDevice objects"""
		# Note: DebugHandler does not discriminate between AdderReceiver and AdderTransmitter
		# So checking for parent class AdderDevice
		# If using on a live server, feel free to check for AdderReceiver

		# We will have to assume there are receivers...
		receivs = list(self.api.getReceivers())
		self.assertGreater(len(receivs), 0)
		
		for rx in receivs:
			self.assertIsInstance(rx, devices.AdderDevice)

	def test_valid_presets(self):
		"""Any presets should be returned as AdderPreset objects"""

		pres = list(self.api.getPresets())
		self.assertGreater(len(pres), 0)

		# We will have to assume there are presets...
		for ps in pres:
			self.assertIsInstance(ps, presets.AdderPreset)
	
	def __del__(self):
		self.api.logout()

if __name__ == "__main__":
	unittest.main()