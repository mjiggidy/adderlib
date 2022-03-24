=========
 Presets
=========

A preset consists of multiple channel/receiver pairs, useful for storing multiple connections together.

In ``adderlib``, a preset is represented by :class:`adderlib.presets.AdderPreset`.  It encapsulates one 
or more :class:`adderlib.presets.AdderPreset.Pair` objects.

Getting Presets
===============

A list of presets available to the user can be retrieved with :meth:`adderlib.adder.AdderAPI.getPresets`.

.. code-block:: python

	# Print all the known presets
	for ps in api.getPresets():
		print(f"{ps.name} has {ps.pair_count} pair(s)")

If the ID of an existing preset is known, it can be provided as an argument, 
and that preset will be the only result returned.

.. code-block:: python

	# Get a preset with a specific ID
	try:
		ps = next(api.getPresets(7))
	except StopIteration:
		print("No preset found with ID 7", sys.stderr)

.. note::
	:meth:`~.adder.AdderAPI.getPresets` always returns a `Generator` of :class:`~.presets.AdderPreset` objects.

Loading a Preset
================

An existing preset can be loaded with :meth:`adderlib.adder.AdderAPI.loadPreset`.  This will connect 
all pairs of receivers and channels.

.. code-block:: python

	# Get a preset and load it
	ps = next(api.getPresets())
	api.loadPreset(
		preset=ps,
		mode=channels.AdderChannel.ConnectionMode.SHARED
	)
	print(f"{ps.name} has been loaded")

An optional named argument ``force`` can be set to `True`, to attempt to force each receiver to disconnect from its current channel 
and connect to the channel from the preset even if the user logged in to that receiver is different than the one issuing the API 
command.  This will only be successsful if the user logged in to the API is an administrator.

Unloading a Preset
==================

A preset can be unloaded with :meth:`adderlib.adder.AdderAPI.unloadPreset` by passing the :meth:`~.presets.AdderPreset` to unload 
as an argument.

.. code-block:: python

	# Get a preset and unload it
	ps = next(api.getPreset())
	api.unloadPreset(ps)
	print(f"{ps.name} has been unloaded")

An optional named argument ``force`` can be set to `True`, to attempt to force each receiver to disconnect from its preset channel 
even if the user logged in to that receiver is different than the one issuing the API command.  This will only be successsful if the 
user logged in to the API is an administrator.

Creating a Preset
=================

A preset can be created from a list of :class:`.AdderPreset.Pair` objects and allowed :class:`.AdderChannel.ConnectionMode` values with :meth:`adderlib.adder.AdderAPI.createPreset`.  
If succesful, the new preset will be returned as an :class:`~.presets.AdderPreset` object.

.. code-block:: python

	# Create a list of trivial channel/receiver pairs
	pairs = list()
	for ch, rx in zip(api.getChannels(), api.getReceivers()):
		pairs.append(presets.AdderPreset.Pair(
			channel=ch,
			receiver=rx
		))
	
	# Create a preset from those pairs
	ps = api.createPreset(
		name="My Cool Preset Wow",
		pairs=pairs,
		modes=[
			channels.AdderChannel.ConnectionMode.VIEW_ONLY,
			channels.AdderChannel.ConnectionMode.SHARED
		]
	)
	print(f"Created preset {ps.name} with ID {ps.id}")

Deleting a Preset
=================

A preset can be deleted with :meth:`adderlib.adder.AdderAPI.deletPreset` by passing the desired :class:`~.channels.AdderChannel` 
as an argument.

.. code-block:: python

	# Delete all presets for fun
	for ps in api.getPresets():
		print(f"Deleting preset {ps.name}")
		api.deletePreset(ps)

.. note::
	This method must be called by an administrator.