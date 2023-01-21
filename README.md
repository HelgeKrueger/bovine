# Bovine

Bovine is attempt at creating a modular ActivityPub server.

## Structure

The current code base is split into a few parts contained in the subpackages.

### bovine

Contains the server / client code to interact with ActivityPub. It uses asyncio using Quart and aiohttp. A basic server implementation using it is available at `examples/basic_app.py`.

You can run it with

```
DOMAIN=my_domain hypercorn examples.basic_app:app --bind 0.0.0.0:3335
```

and then querying using

```
curl http://localhost:3335/.well-known/nodeinfo
curl http://localhost:3335/.well-known/webfinger?resource=acct:test
curl http://localhost:3335/activitypub/test
curl http://localhost:3335/activitypub/test
curl http://localhost:3335/activitypub/test -H accept:application/activity+json
```

### bovine_tortoise

By itself the bovine server does not do much. It mostly just writes things to stdout in reaction to requests. Bovinge_tortoise provides a database layer implemented with tortoise-orm. This allows for elements send to the inbox actually being recorded and an outbox being displayed.

### bovine_blog

This provides an actual webserver on top of bovine + bovine_tortoise. It's look is still firmly basic.

**FIXME**: The current implementation of content negotiation is still too hacky. It occurs inside bovine / bovine_tortoise instead of bovine_blog. This needs to be fixed.

### bovine_admin and bovine_admin_webapp

This provides an user interface to interact with the instance. Basically, it provides a view of the inbox and allows one to empty it, write replies, and compose new posts. The formatting uses markdown.

Note: it is assumed that bovine_admin runs on the same server as bovine_blog, and the resulting service is port forwarded to port 8000 using ssh. See `server.js` for details.
