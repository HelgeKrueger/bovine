# Bovine

Bovine is attempt at creating a modular ActivityPub server.

## Development

Code is tested with `pytest`. Linted with `flake8`. Formatted with `black`. Furthermore some typing is enforced with `mypy`. Imports are sorted using `isort`.

## Structure

The current code base is split into a few parts contained in the subpackages.

### bovine

Contains the server / client code to interact with ActivityPub. It uses asyncio using Quart and aiohttp. A basic server implementation using it is available at `examples/basic_app.py`. It should be noted that this example application does the absolute minimum. It only exposes what is needed to interact with activitypub. Also the user `test` is hard coded in it.

You can run it with

```
poetry run python examples/basic_app.py
```

alternatively you can run it using hypercorn via

```
poetry run hypercorn examples.basic_app:app
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

### bovine_admin and bovine_admin_webapp

This provides an user interface to interact with the instance. Basically, it provides a view of the inbox and allows one to empty it, write replies, and compose new posts. The formatting uses markdown.

Note: it is assumed that bovine_admin runs on the same server as bovine_blog, and the resulting service is port forwarded to port 8000 using ssh. See `server.js` for details.
