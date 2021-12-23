from adderlib import adder
import sys

if len(sys.argv) < 4:
	sys.exit(f"Usage: example.py server_address username password")

api = adder.AdderAPI(sys.argv[1])
api.login(username=sys.argv[2], password=sys.argv[3])

print("\nTransmitters Online:")
for tx in [tx for tx in api.getTransmitters() if tx.status==tx.DeviceStatus.ONLINE]:
	pi = tx.interfaces[0]
	print(f"{tx.name}\t{pi.ip_address}\t{pi.mac_address}\t{tx.status.name}")

print("\nTransmitters Offline:")
for tx in [tx for tx in api.getTransmitters() if tx.status!=tx.DeviceStatus.ONLINE]:
	pi = tx.interfaces[0]
	print(f"{tx.name}\t{pi.ip_address}\t{pi.mac_address}\t{tx.status.name}")

print("\nReceivers Online:")
for tx in [tx for tx in api.getReceivers() if tx.status==tx.DeviceStatus.ONLINE]:
	pi = tx.interfaces[0]
	print(f"{tx.name}\t{pi.ip_address}\t{pi.mac_address}\t{tx.status.name}\t{tx.connection_start}\t{tx.connection_end}")

print("\nReceivers Offline:")
for tx in [tx for tx in api.getReceivers() if tx.status!=tx.DeviceStatus.ONLINE]:
	pi = tx.interfaces[0]
	print(f"{tx.name}\t{pi.ip_address}\t{pi.mac_address}\t{tx.status.name}")

print("")
api.logout()