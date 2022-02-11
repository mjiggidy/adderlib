#!/usr/bin/env python3

import sys, time, typing
from adderlib import adder, presets
from adderlib.channels import AdderChannel

def getChoice(choices:typing.Iterable[str], prompt:typing.Optional[str]=None) -> str:
	"""Prompt user to make a choice"""
	while True:
		try:
			choice = input(prompt)
			if choice in choices: return choice
		except Exception as e:
			continue

def showReceiverMenu(receivers:typing.Iterable[adder.AdderReceiver]) -> adder.AdderReceiver:
	"""Show receiver menu"""
	for idx, rx in enumerate(receivers):
		print(f"{str(idx+1).rjust(3)}: {rx.name}")
	print("  D: Done")
	print("  C: Cancel")
	print("  X: Exit")

	choices = [str(x) for x in range(1,len(list(receivers))+1)]
	choices.extend(["D","X"])
	choice = getChoice(choices, "Choose a receiver: ")

	if choice == "D":
		raise StopIteration
	elif choice == "X":
		sys.exit()
	else:
		return receivers[int(choice) - 1]

def showChannelMenu(channels:typing.Iterable[adder.AdderChannel]) -> adder.AdderChannel:
	"""Show receiver menu"""
	for idx, ch in enumerate(channels):
		print(f"{str(idx+1).rjust(3)}: {ch.name}")
	print("  C: Cancel")
	print("  X: Exit")

	choices = [str(x) for x in range(1,len(list(channels))+1)]
	choices.extend(["C","X"])
	choice = getChoice(choices, "Choose a channel: ")

	if choice == "C":
		raise StopIteration
	elif choice == "X":
		sys.exit()
	else:
		return channels[int(choice) - 1]


if len(sys.argv) < 4:
	sys.exit("Usage: example.py server_address username password")

try:
	api = adder.AdderAPI(sys.argv[1])
	api.login(username=sys.argv[2], password=sys.argv[3])
	if not api.user.logged_in: raise Exception("Did not log in")
except Exception as e:
	sys.exit(f"Unable to log in user {sys.argv[2]}: {e}")


pairs = []

receivers = list(api.getReceivers())
channels = list(api.getChannels())
while True:
	try:
		rx = showReceiverMenu([rx for rx in receivers if rx not in [ps.receiver for ps in pairs]])
		ch = showChannelMenu(channels)
		pairs.append(presets.AdderPreset.Pair(ch, rx))
		print(f"Paired {rx.name} with {ch.name}")
	except StopIteration:
		break

print("New preset will be:")
for ps in pairs:
	print(f"{ps.channel.name}\t-> {ps.receiver.name}")

ps_name = input("Name of preset: ")

try:
	ps = api.createPreset(ps_name, pairs, adder.AdderChannel.ConnectionMode.SHARED)
except Exception as e:
	sys.exit(f"Error creating preset: {e}")

print(f"Successfully created preset {ps.name}")

if getChoice(['Y','N'], "Load now? Y/N: ") == 'Y':
	try:
		api.loadPreset(ps, AdderChannel.ConnectionMode.SHARED, force=True)
	except Exception as e:
		print(f"Couldn't do it: {e}")
	
	print("All set.")
else:
	print("No worries.")

sys.exit()
