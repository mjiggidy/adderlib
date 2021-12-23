# adderlib

`adderlib` is an unofficial python implementation of the Adder API, for use with Adderlink KVM systems.

With `adderlib`, you can:
- Log in or out as an existing KVM user
- Query lists of transmitters, receivers, and channels available to the user
- Access properties many properties of the KVM devices
- Connect receivers to channels
- Manage presets

...and so much more!  Well, a little bit more.


## Customizable

Boy oh boy is this customizable!  An `UrlHandler` abstract class is provided.  Subclass this and override the `api_call()` method to communicate with the server however you wish!  I sure spent a lot of time on the `RequestsHandler` class, which uses the [`requests`](psf/requests) library but that's ok.
