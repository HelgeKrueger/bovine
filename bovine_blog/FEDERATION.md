# Federation

This document is meant to be a reference for all the ActivityPub
federation-related behavior that bovine has. `bovine_blog`
is the only part of this project that is currently meant to
federate.

- Bovine is meant to modular. This also means that it has no specific
  federation behavior, except trying to implement ActivityPub as best as
  possible.
- There is one notable exception: HTTP Signatures. Bovine assumes all
  requests to be signed, except to get the `bovine` Actor object. The
  `bovine` Actor is used to fetch public keys.
- `bovine_blog` actually contains an implementation of federation behavior
  in [processors.py](bovine_blog/processors.py). My goal is to make
  this file human readable.
- Activities are passed to the client by default through Client to Server.
