# Bovine Core

The core of bovine. This is intended to be sufficient to build
an ActivityPub Client application. There are currently three
things covered:

- `bovine_core.activitystreams` contains builders to create
 [ActivityStreams](https://www.w3.org/ns/activitystreams) objects.
- `bovine_core.clients` contains routines to interact with
 ActivityPub servers. In particular, routines to perform
 POST and GET requests using HTTP Signatures are implemented.
- `bovine_core.utils` contains the cryptographic stuff to
 handle HTTP Signatures.
