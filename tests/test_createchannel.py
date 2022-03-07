import sys
from adderlib import adder

if len(sys.argv)<4:
	sys.exit(f"Usage: {__file__} server username password")

address, username, password = sys.argv[1:4]

api = adder.AdderAPI(address)
api.login(username, password)

tx = next(api.getTransmitters())
print(f"Got transmitter {tx.name}")

try:
	new_ch = api.createChannel("Test Channel", "Testing dat channel", "MyMind", video1=tx, group_name="MCPs")
	print(f"Created channel {new_ch.name} with id {new_ch.id} and transmitters {new_ch.tx_id}")
except Exception as e:
	print("Could not create channel:",str(e))

api.logout()