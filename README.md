# Bovine

Bovine is attempt at creating a modular ActivityPub server.

## Implementation notes

- [Actor objects](docs/actor.md)
- [HTTP Signatures](docs/http_signatures.md)
- [Client2Server ActivityPub](docs/client_to_server_activitypub.md)
- [Like Activity](docs/like_activity.md)
- [Deployment](docs/deployment.md)

## Development

Code is tested with `pytest`. Linted with `flake8`. Formatted with `black`. Furthermore some typing is enforced with `mypy`. Imports are sorted using `isort`.

## Structure

The current code base is split into packages with more and more complicated use cases.

### bovine_core

This package contains the basic code necessary to build an activity pub client application.
A big caveat here is that currently authentication is assumed to be done through HTTP
signatures. It considers essentially of two parts:

`bovine_core.clients.signed_http` provides the functions `signed_get` and `signed_post`,
which are used to communicate with the webserver. The package `bovine_core.activitystreams`
contains builder used to construct the necessary [ActivityStreams objects](https://www.w3.org/ns/activitystreams).

### Examples

Two examples are included in the `examples` folder:

- Munching cow demonstrates how to post simple content in `munching_cow.py` and then clean it back up in `munching_cow_cleanup.py`.

- Cow Resisa provides a sample RSS to ActivityPub bridge.

### bovine

Contains the server / client code to interact with ActivityPub. It uses asyncio using Quart and aiohttp.

#### Examples

A basic server implementation using it is available at `examples/basic_app/basic_app.py`. It should be noted that this example application does the absolute minimum. It only exposes what is needed to interact with activitypub. Also the user `test` is hard coded in it.

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

By itself the bovine server does not do much. It mostly just writes things to stdout in reaction to requests. Bovinge_tortoise provides a database layer implemented with tortoise-orm. This allows for elements send to the inbox actually being recorded and an outbox being displayed. The database is currently managed with `aerich`.

### bovine_blog

This provides an actual webserver on top of bovine + bovine_tortoise. It's look is still firmly basic. The HTML layouting and content presentation of the blog application can be developped independent of the rest of `bovine` by running

```
poetry run hypercorn examples.local_test_blog:app
```

The provided content is hard coded in `examples/local_test_blog.py`. Due to the nature of http signatures. The ids of posts correspond to the ActivityPub objects, e.g. `https://my_domain/activitypub/test/1234-5678`. The current implementation redirects requests to these urls not having the accept type matching `application/.*json` to `https://my_domain/test/1234-5678`.

`bovine_blog/scripts` contains some scripts that were useful during testing and development. In particular

```
poetry run python bovine_blog/scripts/add_user.py USERNAME
```

can be used to create new users including public/private keys.

### buffalo

Buffalo is an attempt at writing a webapp able to interact with bovine through ActivityPub Client to Server.
It uses ReactJS for frontend management and JSX to give the code some kind of structure. Data is stored
client side using dexie.js. Features included

- Threaded conversation view. Already seen elements are collapsed
- On mobile: Swipe left for next conversation
- Composing both replies / and new new posts
- Liking

ActivityPub activities are currently created in the frontend.

#### Configuration

Currently, the authorization and used user are hardcoded in `buffalo/src/config.js`.

#### Development

`npm` is used for package management. The root directory with the package files is `buffalo`.

There are some `jest` tests. Code is formatted with `prettier`. Source can be linted with `eslint`.
