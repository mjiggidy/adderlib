import unittest
from adderlib import adder, users, channels, devices, urlhandlers

class TestAuthentication(unittest.TestCase):

	def test_valid_login(self):
		user = users.AdderUser()
		ad = adder.AdderAPI(user=user, url_handler=urlhandlers.DebugHandler(), api_version=8)
		ad.login("test","goodpwd")
		self.assertTrue(user.logged_in)
		self.assertFalse(user.logged_out)
	
	def test_invalid_login(self):
		user = users.AdderUser()
		ad = adder.AdderAPI(user=user, url_handler=urlhandlers.DebugHandler(), api_version=8)
		ad.login("test","badpwd")
		self.assertFalse(user.logged_in)
		self.assertTrue(user.logged_out)
	
	def test_valid_logout(self):
		user = users.AdderUser()
		ad = adder.AdderAPI(user=user, url_handler=urlhandlers.DebugHandler, api_version=8)
		ad.login("test","goodpwd")
		self.assertTrue(user.logged_in)
		ad.logout()
		self.assertTrue(user.logged_out)
		self.assertFalse(user.logged_in)
	
class TestDevices(unittest.TestCase):

	def test_valid_transmitter(self):
		user = users.AdderUser()
		ad = adder.AdderAPI(user=user, url_handler=urlhandlers.DebugHandler(), api_version=8)
		ad.login("test","goodpwd")
		
		tx = next(ad.getTransmitters())
		self.assertIsInstance(tx, devices.AdderTransmitter)
		self.assertTrue(tx, tx.interfaces[0].is_online)
	
	def test_valid_receiver(self):
		user = users.AdderUser()
		ad = adder.AdderAPI(user=user, url_handler=urlhandlers.DebugHandler(), api_version=8)
		ad.login("test","goodpwd")

		rx = next(ad.getReceivers())
		self.assertIsInstance(rx, devices.AdderReceiver)
		self.assertTrue(rx, rx.is_connected)
	

class TestChannels(unittest.TestCase):

	def test_valid_channel(self):
		user = users.AdderUser()
		ad = adder.AdderAPI(user=user, url_handler=urlhandlers.DebugHandler(), api_version=8)
		ad.login("test","goodpwd")

		chan = next(ad.getChannels())
		self.assertIsInstance(chan, channels.AdderChannel)

if __name__ == "__main__":
	unittest.main()