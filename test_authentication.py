import unittest
from adderlib import adder

class TestAuthentication(unittest.TestCase):

    def test_valid_login(self):
        user = adder.AdderUser()
        ad = adder.AdderAPI(user=user, url_handler=adder.DebugHandler(), api_version=8)
        ad.login("test","goodpwd")
        self.assertTrue(user.logged_in)
        self.assertFalse(user.logged_out)
    
    def test_invalid_login(self):
        user = adder.AdderUser()
        ad = adder.AdderAPI(user=user, url_handler=adder.DebugHandler(), api_version=8)
        ad.login("test","badpwd")
        self.assertFalse(user.logged_in)
        self.assertTrue(user.logged_out)

if __name__ == "__main__":
    unittest.main()