===============
 Adder Devices 
===============

Adderlink devices can be queried and manipulated by an active Adderlink API session logged in with a valid user.  
See :doc:`connection` for details on how to establish a connection.

Transmitters
============

In ``adderlib``, an Adderlink transmitter is represented by :class:`adderlib.devices.AdderTransmitter`.

Getting Transmitters
--------------------

A list of transmitters available to the user can be retrieved with :meth:`adderlib.adder.AdderAPI.getTransmitters`.

.. code-block:: python

	for tx in api.getTransmitters():
		print(tx.id, tx.name)

If the ID for a transmitter is known, it can be provided as an argument and that transmitter will be the only result:

.. code-block:: python

	try:
		tx = next(api.getTransmitters(420))
	except StopIteration:
		print("No transmitter found with ID 80085", sys.stderr)

.. note::
	:meth:`~.adder.AdderAPI.getTransmitters` always returns a `Generator` of :class:`~.devices.AdderTransmitter` objects.


Receivers
=========

In ``adderlib``, an Adderlink receiver is represented by :class:`adderlib.devices.AdderReceiver`.

Getting Receivers
-----------------

A list of receivers available to the user can be retrieved with :meth:`adderlib.adder.AdderAPI.getReceivers`.

.. code-block:: python

	for rx in api.getReceivers():
		print(rx.id, rx.name)

If the ID for a receiver is known, it can be provided as an argument and that receiver will be the only result:

.. code-block:: python

	try:
		rx = next(api.getReceiver(690))
	except StopIteration:
		print("No receiver found with ID 690", sys.stderr)

.. note::
	:meth:`~.adder.AdderAPI.getReceivers` always returns a `Generator` of :class:`~.devices.AdderReceiver` objects.

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