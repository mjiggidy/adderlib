=======================
 Connections and Users
=======================

Establishing a Server Connection
================================

Initializing the API
--------------------

To begin using the Adder API, first an :class:`adderlib.adder.AdderAPI` object should be created.  The only required argument is the IP address or hostname of the AIM (Adder Infinity Manager) server, 
although providing an API Version as a named argument is recommended:

.. code-block:: python

	from adderlib import adder
	api = adder.AdderAPI("192.168.0.1", api_version=8)

In special cases, a custom URL handler may be desired.  An instance of the custom URL handler can be passed as the named argument ``url_handler``.  See `Custom URL Handlers`_ for more information.

Logging In
----------

With the Adder API object created, a session can be created by logging in as a user with :meth:`adderlib.adder.AdderAPI.login`.  The username and password passed to this method should correspond to an 
existing KVM user account set up on the AIM.

.. code-block:: python

	api.login(username="timmy", password="wh0b33f3d?")

.. note::
	
	Adder's permissions system applies even to the API.  For example, if a user's account is only permitted access to certain channels for normal KVM usage, only those channels will be 
	accessible to him via the API as well.  So, depending on what needs to be accomplished via the API, an admin account may be necessary for certain operations.

Once an API connection has been established with a valid user, the rest of the ``adderlib`` API can be used.

URL Handlers
============

Default Handler
---------------

The default URL handler for issuing HTTP GET requests to Adder's REST API is :class:`adderlib.urlhandlers.RequestsHandler`.  This uses the third-party `Requests <https://github.com/psf/requests>`_ module 
and should be suitable for most cases.

Custom URL Handlers
-------------------
For special circumstances where the ``requests`` module is not available or unwanted, ``adderlib`` provides an abstract class :class:`adderlib.urlhandlers.UrlHandler` 
which may be subclassed.  In this case, the class method :meth:`adderlib.urlhandlers.UrlHandler.api_call` must be overridden with the desired functionality.