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

## Examples and toml file format

The two examples in the example folder currently rely on a configuration file
called `helge.toml`.

```toml
account_url = "https://mymath.rocks/activitypub/helge"
public_key_url = "https://mymath.rocks/activitypub/helge#main-key"
private_key = """-----BEGIN PRIVATE KEY-----
...
-----END PRIVATE KEY-----
"""
```

__FIXME__: Use hello.coop to provide oauth support.

The two scripts are `examples/sse.py` which opens the event source for the inbox
and displays new elements. The second script `examples/send_note.py` allows one
to send a quick message. Example usage:

```shell
poetry run python examples/send_note.py 'Hello World! via send_note.py and AP-C2S.'
```

Similary the script `examples/send_like.py` can be used to like a remote object

```shell
poetry run python examples/like.py ID_OF_REMOTE_OBJECT
```
