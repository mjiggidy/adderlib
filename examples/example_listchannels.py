import sys, typing
from adderlib import adder, devices

def tx_from_id(devices:list[devices.AdderTransmitter], id:str) -> typing.Optional[devices.AdderTransmitter]:
	for tx in devices:
		if tx.id == id:
			return tx
	
	return None

if len(sys.argv) < 4:
	sys.exit(f"Usage: {__file__} server_address username password")

address, username, password = sys.argv[1:4]

try:
	api = adder.AdderAPI(address)
	api.login(username=username, password=password)
except adder.AdderRequestError as e:
	sys.exit(f"Unable to log in user ({e})")
except Exception as e:
	sys.exit(f"Unable to connect to the Adder manager ({e.__class__.__name__})")

trans = list(api.getTransmitters())

print(f"\nChannels available to {api.user.username}:\n")

# Don't judge me here
print(str().join([str(x).ljust(24) for x in [
	"Channel",
	"Description",
	"Location",
	"Status",
	"Transmitter",
	"Shortcut"
]]))

print("="*24*6)

for ch in api.getChannels():

	print(str().join([str(x).ljust(24) for x in [
		ch.name,
		ch.description,
		ch.location,
		"Online" if ch.is_online else "Offline",
		tx_from_id(trans, ch.tx_id).name,
		ch.shortcut
	]]))


print("")
api.logout()