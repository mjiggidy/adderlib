.. adderlib documentation master file, created by
   sphinx-quickstart on Wed Mar 16 18:21:59 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

==========
 adderlib
==========


Welcome to adderlib's documentation!
====================================

.. toctree::
   :caption: Usage Guide
   :maxdepth: 1
   
   connection
   devices
   channels
   presets

.. toctree::
   :caption: Module Definitions

   adderlib.adder
   adderlib.channels
   adderlib.devices
   adderlib.presets


About the Library
=================

``adderlib`` is an unofficial python wrapper for the `Adder API <https://support.adder.com/tiki/tiki-index.php?page=ALIF%3A%20API>`_, for use with Adderlink KVM systems.

With ``adderlib``, you can:

* Log in or out as an existing KVM user
* Query lists of transmitters, receivers, and channels available to the user
* Access many properties of the KVM devices
* Connect receivers to channels
* Manage presets

\...and so much more!  Well, a little bit more.

Getting Started
===============

The best way to get started is to check out the `examples on GitHub <https://github.com/mjiggidy/adderlib/tree/master/examples>`_, but in general, it's four easy steps:

.. code-block:: python
   :caption: cool-printer-extreme.py
   :linenos:

   from adderlib import adder

   # Step 1: Create a handle to the API by passing
   # the IP address or hostname of the AIM (the KVM server)
   api = adder.AdderAPI("192.168.1.10")

   # Step 2: Log in using an exising KVM account
   api.login("username","password")

   # Step 3: Do some stuff
   for tx in api.getTransmitters():
      print(tx.name)

   # Step 4: Don't forget to log out!
   api.logout()

Next Steps
==========

For more in-depth usage information, start with :doc:`connection`.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
