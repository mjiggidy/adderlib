===============
 Adder Devices 
===============

Adderlink devices can be queried and manipulated by an active Adderlink API session logged in with a valid user.  
See :doc:`connection` for details on how to establish a connection.

Transmitters
============

In ``adderlib``, an Adderlink transmitter is represented by :class:`adderlib.devices.AdderTransmitter`.

:class:`~.devices.AdderTransmitter` inherits from base class :class:`adderlib.devices.AdderDevice`, which exposes 
more useful properties to be aware of.

Getting Transmitters
--------------------

A list of transmitters available to the user can be retrieved with :meth:`adderlib.adder.AdderAPI.getTransmitters`.

.. code-block:: python

	for tx in api.getTransmitters():
		print(tx.id, tx.name)

If the ID for a transmitter is known, it can be provided as an argument and that transmitter will be the only result:

.. code-block:: python

	try:
		tx = next(api.getTransmitters(23))
	except StopIteration:
		print("No transmitter found with ID 23", sys.stderr)

.. note::
	:meth:`~.adder.AdderAPI.getTransmitters` always returns a `Generator` of :class:`~.devices.AdderTransmitter` objects.

Modifying Transmitters
----------------------

A transmitter's description and location information can be modified using :meth:`adderlib.adder.AdderAPI.setDeviceInfo` by 
passing the relevant :class:`~.devices.AdderTransmitter` object, and ``description`` and/or ``location`` strings as named 
arguments.

.. code-block:: python

	for idx, tx in enumerate(api.getTransmitters()):
		api.setDeviceInfo(
			tx,
			location="Bathroom",
			description=f"Transmitter from Toilet Maintanence Interface {idx+1}"
		)

If either ``description`` or ``location`` arguments are omitted, the existing information for that argument will remain 
the same.  Pass an empty string to truly clear it out.


Receivers
=========

In ``adderlib``, an Adderlink receiver is represented by :class:`adderlib.devices.AdderReceiver`.

:class:`~.devices.AdderReceiver` inherits from base class :class:`adderlib.devices.AdderDevice`, which exposes 
more useful properties to be aware of.

Getting Receivers
-----------------

A list of receivers available to the user can be retrieved with :meth:`adderlib.adder.AdderAPI.getReceivers`.

.. code-block:: python

	for rx in api.getReceivers():
		print(rx.id, rx.name)

If the ID for a receiver is known, it can be provided as an argument and that receiver will be the only result:

.. code-block:: python

	try:
		rx = next(api.getReceiver(42))
	except StopIteration:
		print("No receiver found with ID 42", sys.stderr)

.. note::
	:meth:`~.adder.AdderAPI.getReceivers` always returns a `Generator` of :class:`~.devices.AdderReceiver` objects.


Modifying Receivers
-------------------

A receiver's description and location information can be modified using :meth:`adderlib.adder.AdderAPI.setDeviceInfo` by 
passing the relevant :class:`~.devices.AdderReceiver` object, and ``description`` and/or ``location`` strings as named 
arguments.

.. code-block:: python

	for idx, rx in enumerate(api.getReceivers()):
		api.setDeviceInfo(
			rx,
			location="Break Room",
			description=f"Receiver {idx+1} for lunch work"
		)

If either ``description`` or ``location`` arguments are omitted, the existing information for that argument will remain 
the same.  Pass an empty string to truly clear it out.

AIM Servers
===========

In ``adderlib``, an AIM server is represented by :class:`adderlib.devices.AdderServer`.

Getting Servers
---------------

A list of servers available to the user can be retrieved with :meth:`adderlib.adder.AdderAPI.getServers`.

.. code-block:: python

	for srv in api.getServers():
		print(srv.name, srv.role)

.. note::
	:meth:`~.adder.AdderAPI.getServers` always returns a `Generator` of :class:`~.devices.AdderServer` objects.

.. note::
	Unlike :class:`~.devices.AdderTransmitter` or :class:`~.devices.AdderReceiver`, :class:`~.devices.AdderServer` 
	does not inherit from the base class :class:`~.devices.AdderDevice`, so many common attributes like ``id`` are not available.

Next Steps
==========

Now that we know how to work with Adder devices, we can use them to create and connect to :doc:`channels` and :doc:`presets`.