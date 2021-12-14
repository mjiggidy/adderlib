#!/usr/bin/env python3

from adderlib import adder, urlhandlers
import sys, getpass

class NoDevicesFound(Exception):
	"""No devices were returned in a query"""

def promptChannels(api:adder.AdderAPI) -> adder.AdderChannel:
	"""Request a specific transmitter"""
	channels = [x for x in api.getChannels() if x.is_online]
	if not len(channels):
		raise NoDevicesFound("No channels were found to be online.")
	
	for idx, ch in enumerate(channels):
		print(f"{str(idx+1).rjust(3)}: {ch.name}")
	
	while True:
		try:
			choice = int(input("Choose a channel: ").strip()) - 1
		except Exception as e:
			continue
		if -1 < choice < len(channels):
			return channels[choice]

def promptReceivers(api:adder.AdderAPI) -> adder.AdderReceiver:
	"""Request a specific transmitter"""
	receivers = [x for x in api.getReceivers() if x.status is x.status.ONLINE]

	for idx, rx in enumerate(receivers):
		print(f"{str(idx+1).rjust(3)}: {rx.name}")
	if not len(receivers):
		raise NoDevicesFound("No receivers were found to be online.")

	while True:
		try:
			choice = int(input("Choose a receiver: ").strip()) - 1
		except Exception as e:
			continue
		if -1 < choice < len(receivers):
			return receivers[choice]
	
print(f"Please log in to continue")

# Get address from args, if provided; otherwise prompt
address = sys.argv[1] if len(sys.argv) > 1 else None
if address is None:
	while True:
		address = input("Server [address:port]: ").strip()
		if len(address):
			break

# Get credentials
while True:
	username = input("Username: ")
	if len(username):
		break
while True:
	password = getpass.getpass("Password: ")
	if len(password):
		break

# Try to log in
req = urlhandlers.RequestsHandler(address)
api = adder.AdderAPI(url_handler=req)
api.login(username=username, password=password)

if not api.user.logged_in:
	sys.exit(f"Unable to log in to {api.url_handler.server_address} as {username}")

print(f"Logged in to {api.url_handler.server_address} as {api.user.username}\n")

# Select receiver
print("Receivers:")
try:
	choice_rx = promptReceivers(api)
except NoDevicesFound as e:
	api.logout()
	sys.exit(str(e))
print(f"Selected {choice_rx.name}\n")

# Select channel
print("Channels:")
try:
	choice_ch = promptChannels(api)
except NoDevicesFound as e:
	api.logout()
	sys.exit(str(e))
print(f"Selected {choice_ch.name}\n")

# Connect the receiver to the channel
print(f"Connecting {choice_ch.name} to {choice_rx.name}...")
api.connectToChannel(choice_ch, choice_rx)
print("Done.")

# Log out
api.logout()
print("\nLogged out" if api.user.logged_out else "\nCould not log out")