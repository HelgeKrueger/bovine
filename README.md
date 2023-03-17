# Bovine

Bovine is a set of packages that simplify working with [ActivityPub](https://www.w3.org/TR/activitypub/). The design goal is to provide an architecture that allows one to replace certain parts. For example the package [bovine_store](bovine_store) contains as the name indicates the data store being used. If the architecture was properly modular, it should be possible to replace bovine_store with a different implementation, without having to change anything in the rest of the code. I don't think I have met this goal yet, but in this sense bovine should be _modular_.

__FIXME__

## Implementation notes

- [Actor objects](docs/actor.md)
- [HTTP Signatures](docs/http_signatures.md)
- [Client2Server ActivityPub](docs/client_to_server_activitypub.md)
- [Like Activity](docs/like_activity.md)
- [Deployment](docs/deployment.md)

## Development

Code is tested with `pytest`. Linted with `flake8`. Formatted with `black`. Furthermore some typing is enforced with `mypy`. Imports are sorted using `isort`. All the tests can be run via

```bash
./all_tests.sh
```

## Structure

The current codebase is split into packages with incrementally more complex use cases.

### bovine_core

The `bovine_core` package contains the basic code necessary to build an ActivityPub client application.
A big caveat here is that currently authentication is assumed to be done through HTTP
signatures. It consists essentially of two parts:

`bovine_core.clients.signed_http` provides the functions `signed_get` and `signed_post`
which are used to communicate with the webserver, and `bovine_core.activitystreams`
contains builders used to construct the necessary [ActivityStreams objects](https://www.w3.org/ns/activitystreams).

### Examples

Two examples are included in the `examples` folder:

- Munching cow demonstrates how to post simple content in `munching_cow.py` and then clean it back up in `munching_cow_cleanup.py`.

- Cow Resisa provides a sample RSS to ActivityPub bridge.

### bovine

The `bovine` package contains the server / client code to interact with ActivityPub. It uses asyncio using Quart and aiohttp.

#### Examples

A basic server implementation using it is available at `examples/basic_app/basic_app.py`. It should be noted that this example application does the absolute minimum. It only exposes what is needed to interact with ActivityPub. Also the user `test` is hard coded in it.

You can run it with

```
cd examples/basicapp
poetry run python basic_app.py
```

alternatively you can run it using hypercorn via

```
poetry run hypercorn basic_app:app
```

and then querying using

```
curl http://localhost:3335/.well-known/nodeinfo
curl http://localhost:3335/.well-known/webfinger?resource=acct:test
curl http://localhost:3335/activitypub/test
curl http://localhost:3335/activitypub/test -H accept:application/activity+json
```

### bovine_tortoise

By itself the bovine server does not do much: mostly just writeing things to stdout in reaction to requests. The `bovine_tortoise` package provides a database layer implemented with tortoise-orm. This allows for elements sent to the inbox to actually be recorded and for an outbox to be displayed. The database is currently managed with `aerich`.

### bovine_blog

The `bovine_blog` package provides an actual webserver on top of `bovine` + `bovine_tortoise`. Its look is still firmly basic. The HTML layouting and content presentation of the blog application can be developped independent of the rest of `bovine` by running:

```
cd examples/local_test_blog
poetry run hypercorn local_test_blog:app
```

The provided content is hardcoded in `examples/local_test_blog/local_test_blog.py`. Due to the nature of http signatures, the ids of posts correspond to the ActivityPub objects' canonical URI, e.g. `https://my_domain/activitypub/test/1234-5678`. The current implementation redirects requests to these urls not having the accept type matching `application/.*json` to `https://my_domain/test/1234-5678`.

`bovine_blog/scripts` contains some scripts that were useful during testing and development. In particular

```
poetry run python bovine_blog/scripts/add_user.py USERNAME
```

can be used to create new users including public/private keys.
