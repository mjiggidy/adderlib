import sys, random
from adderlib import adder

if len(sys.argv)<4:
	sys.exit(f"Usage: {__file__} server username password")

address, username, password = sys.argv[1:4]

api = adder.AdderAPI(address)
api.login(username, password)

txs = random.sample(list(api.getTransmitters()),2)


try:
	new_ch = api.createChannel(f"{txs[0].name} + {txs[1].name}", "Testing dat channel", "Eng", video1=txs[0], video2=txs[1], group_name="MCPs")
	print(f"Created channel {new_ch.name} with id {new_ch.id} and transmitters {new_ch.tx_id}")
except Exception as e:
	print("Could not create channel:",str(e))



print("k")

api.logout()