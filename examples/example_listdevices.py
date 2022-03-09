import sys
from adderlib import adder

if len(sys.argv) < 4:
	sys.exit(f"Usage: {__file__} server_address username password")

try:
	api = adder.AdderAPI(sys.argv[1])
	api.login(username=sys.argv[2], password=sys.argv[3])
except adder.AdderRequestError as e:
	sys.exit(f"Unable to log in user ({e})")
except Exception as e:
	sys.exit(f"Unable to connect to the Adder manager ({e.__class__.__name__})")

print("\nTransmitters Online:")
for dev in [dev for dev in api.getTransmitters() if dev.status==dev.DeviceStatus.ONLINE]:
	pi = dev.network_interfaces[0]
	print(f"{dev.name.ljust(20)}{dev.model.name.ljust(16)}{str(pi.ip_address).ljust(16)}{pi.mac_address.ljust(20)}{dev.status.name}")

print("\nTransmitters Offline:")
for dev in [dev for dev in api.getTransmitters() if dev.status!=dev.DeviceStatus.ONLINE]:
	pi = dev.network_interfaces[0]
	print(f"{dev.name.ljust(20)}{dev.model.name.ljust(16)}{str(pi.ip_address).ljust(16)}{pi.mac_address.ljust(20)}{dev.status.name}")

print("\nReceivers Online:")
for dev in [dev for dev in api.getReceivers() if dev.status==dev.DeviceStatus.ONLINE]:
	pi = dev.network_interfaces[0]
	print(f"{dev.name.ljust(20)}{dev.model.name.ljust(16)}{str(pi.ip_address).ljust(16)}{pi.mac_address.ljust(20)}{dev.status.name.ljust(10)}{dev.current_username}")

print("\nReceivers Offline:")
for dev in [dev for dev in api.getReceivers() if dev.status!=dev.DeviceStatus.ONLINE]:
	pi = dev.network_interfaces[0]
	print(f"{dev.name.ljust(20)}{dev.model.name.ljust(16)}{str(pi.ip_address).ljust(16)}{pi.mac_address.ljust(20)}{dev.status.name.ljust(10)}{dev.current_username}")

print("")
api.logout()