import sys, typing
from adderlib import adder, devices

def tx_from_id(devices:list[devices.AdderTransmitter], id:str) -> typing.Optional[devices.AdderTransmitter]:
	for tx in devices:
		if tx.id == id:
			return tx
	
	return None

if len(sys.argv) < 4:
	sys.exit(f"Usage: {__file__} server_address username password")

try:
	api = adder.AdderAPI(sys.argv[1])
	api.login(username=sys.argv[2], password=sys.argv[3])
except adder.AdderRequestError as e:
	sys.exit(f"Unable to log in user ({e})")
except Exception as e:
	sys.exit(f"Unable to connect to the Adder manager ({e.__class__.__name__})")

trans = list(api.getTransmitters())

# Don't judge me here
print(f"{'Channel'.ljust(30)}{'Description'.ljust(20)}{'Location'.ljust(20)}{'Status'.ljust(9)}{'Transmitter'.ljust(20)}{'Shortcut'}")
print("="*108)

for ch in api.getChannels():
	print(f"{ch.name.ljust(30)}{ch.description.ljust(20)}{ch.location.ljust(20)}{'Online   ' if ch.is_online else 'Offline  '}{str(tx_from_id(trans,ch.tx_id).name or '').ljust(20)}{ch.shortcut}")

print("")
api.logout()