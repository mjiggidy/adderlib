==========
 Channels 
==========

An Adderlink channel is composed of one or more transmitter sources, and can be connected to by one or more receivers.
See :doc:`devices` for details on how to query transmitters and receivers.

In ``adderlib``, an Adderlink channel is represented by :class:`adderlib.channels.AdderChannel`.

Getting Channels
----------------

A list of channels available to the user can be retrieved with :meth:`adderlib.adder.AdderAPI.getChannels`.

.. code-block:: python

	# Print all the known channels
	for ch in api.getChannels():
		print(ch.id, ch.name)

If the ID or the name of an existing channel is known, either of these can be passed to the method as a named argument, 
and that channel will be the only result returned.

.. code-block:: python

	# Get the channel named "Workstation 01"
	try:
		ch = next(api.getChannels(name="Workstation 01"))
	except StopIteration:
		print("No channel found with name \"Workstation 01\"", sys.stderr)

Connecting to a Channel
-----------------------

A channel can be connected to a receiver with :meth:`adderlib.adder.AdderAPI.connectToChannel` by passing the desired 
:class:`~.channels.AdderChannel` and :class:`~.devices.AdderReceiver` as arguments.

.. code-block:: python

	# Irresponsibly connect a bunch of receivers to channels
	for rx, ch in zip(api.getReceivers(), api.getChannels()):
		print(f"Connecting {ch.name} to {rx.name}")
		api.connectToChannel(channel=ch, receiver=rx)

An optional named argument ``mode`` can be given a named value from the :class:`adderlib.channels.AdderChannel.ConnectionMode` enum.

.. note::
	For more information on working with Adder receivers, see :doc:`devices`.

Disconnecting from a Channel
----------------------------

A channel can be disconnected from a receiver with :meth:`adderlib.adder.AdderAPI.disconnectFromChannel` by passing the desired 
:class:`~.devices.AdderReceiver` as an argument.

.. code-block:: python

	# Disconnect all receivers
	for rx in api.getReceivers():
		if rx.is_connected:
			print(f"Disconnecting {rx.name} from {rx.channel_name}")
			api.disconnectFromChannel(rx)

An optional named argument ``force`` can be set to `True`, to attempt to force the receiver to disconnect even if the 
user logged in to that receiver is different than the one issuing the API command to disconnect.  This will only be successsful if 
the user logged in to the API is an administrator.

Creating a Channel
------------------

A new channel can be created with :meth:`adderlib.adder.AdderAPI.createChannel` by passing at least a channel name as a string.  
If succesful, the new channel will be returned as an :class:`~.channels.AdderChannel` object.

There are many optional named arguments that can be given:

.. automethod:: adderlib.adder.AdderAPI.createChannel
	:noindex:

	:param str name: The channel name
	:param str location: The location of the channel
	:param str group_name: Specify a Channel Group name the new channel should be added to

	:param ~adderlib.devices.AdderTransmitter video1: The transmitter to display on the receiver's first monitor
	:param int video1_head: The display input to use from the source transmitter

	:param ~adderlib.devices.AdderTransmitter video2: The transmitter to display on the receiver's second monitor
	:param int video2_head: The display input to use from the source transmitter

	:param ~adderlib.devices.AdderTransmitter audio: The transmitter to use for the audio source
	:param ~adderlib.devices.AdderTransmitter usb: The transmitter to use for USB devices
	:param ~adderlib.devices.AdderTransmitter serial: The transmitter to use for serial devices

	:param list(~adderlib.channels.AdderChannel.ConnectionMode) modes: A list of connection modes this channel should support

While this method allows for a very granular configuration, in practice this is usually simpler:

.. code-block:: python

	# Create a channel from one transmitter
	tx = next(api.getTransmitters())
	ch = api.createChannel(
		name="Darkweb Station 1",
		location="Bunker 12",
		video1=tx,
		group_name="Top Secret Operations"
	)
	print(f"The channel {ch.name} has been created with ID {ch.id} using sources from {tx.name}")

In this example, the same transmitter is used for all video, audio, USB, and serial sources.  Since no :class:`~.ConnectionMode` list was 
given, the allowed connection modes for this channel will be inherited based on Adder's permissions system.

.. note::
	For more information on working with Adder transmitters, see :doc:`devices`.


Deleting a Channel
------------------

A channel can be deleted with :meth:`adderlib.adder.AdderAPI.deleteChannel` by passing the desired :class:`~.channels.AdderChannel` 
as an argument.

.. code-block:: python

	# Delete all channels for fun
	for ch in api.getChannels():
		print(f"Deleting channel {ch.name}")
		api.deleteChannel(ch)

.. note::
	This method must be called by an administrator.