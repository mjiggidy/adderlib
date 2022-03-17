# adderlib

`adderlib` is an unofficial python implementation of the [Adder API](https://support.adder.com/tiki/tiki-index.php?page=ALIF%3A%20API), for use with Adderlink KVM systems.

With `adderlib`, you can:
- Log in or out as an existing KVM user
- Query lists of transmitters, receivers, and channels available to the user
- Access many properties of the KVM devices
- Connect receivers to channels
- Manage presets

...and so much more!  Well, a little bit more.


## Getting Started

The best way to get started is to check out the [examples](examples/), and then the [official documentation on ReadTheDocs](http://adderlib.readthedocs.io/).  But in general, it's four easy steps:

```python
from adderlib import adder

# Step 1: Create a handle to the API by passing the IP address or hostname of the AIM (the KVM server)
api = adder.AdderAPI("192.168.1.10")

# Step 2: Log in using an exising KVM account
api.login("username","password")

# Step 3: Do some stuff
for tx in api.getTransmitters():
  do_some_stuff(tx)
  
# Step 4: Don't forget to log out!
api.logout()
```

## Customizable

Boy oh boy is this customizable!  An `UrlHandler` abstract class is provided.  Subclass this and override the `api_call()` method to communicate with the server however you wish!  I sure spent a lot of time on the default `RequestsHandler` class, which uses the [`requests`](https://github.com/psf/requests) library but that's ok I'm sure you have your reasons.
