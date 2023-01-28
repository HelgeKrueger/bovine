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

# Implementation notes

## ActivityPub Client 2 Server

The ReactJS web frontend `buffalo` speaks with the python `bovine` running on a server using a "version" of [client to server activity pub](https://www.w3.org/TR/activitypub/#client-to-server-interactions). At least that is the goal.

### Posting

Posting is done pretty much as explained in the document. I'm still deciding what authentication is best. For the [munching cow](https://mymath.rocks/munchingcow), a version of http signatures is used. For the web frontend currently hard coded access tokens are used.

Something like a Like currently requires a "to" field.

```
{
  "@context": "https://www.w3.org/ns/activitystreams",
  "type": "Like",
  "id": "https://mymath.rocks/activitypub/helge/....",
  "actor": "https://mymath.rocks/activitypub/helge",
  "object": "https://mas.to/users/helgek/...",
  "to": [
    "https://mas.to/users/helgek"
  ]
}
```

This is a difference to what Mastodon sends out. Note Mastodon's implementation without a to is suspect.

I plan to implement file uploads as `multipart/form-encoded`. This means that there will be a single request to upload a post with a picture.

### Reading

My current plan is to allow an authorized GET on the inbox, e.g.

```
GET https://mymath.rocks/activitypub/helge/inbox
```

This will then return an [OrderedCollection](https://www.w3.org/TR/activitypub/#inbox) as specified in the spec. I will probably include a new link type that allows one to fetch newer items, e.g.

```
{
    "@context": "https://www.w3.org/ns/activitystreams",
    "nextUpdates": "https:/mymath.rocks/activitypub/helge/inbox?min_id=1235",
    "first": "https:/mymath.rocks/activitypub/helge/inbox?max_id=1234",
    "id": "mymath.rocks/activitypub/helge/inbox",
    "last": "mymath.rocks/activitypub/helge/inbox?min_id=0",
    "totalItems": 446,
    "type": "OrderedCollection"
}

```

or something similar.

### Fetching

This is a new endpoint of the form

```
POST https://mymath.rocks/activitypub/helge/fetch
```

which allows one to fetch remote resources. Current support is for fetching an url. This means that I can copy the URL of a post on the Fediverse and reply to it using Buffalo. The current process still involves quite a bit of copy and pasting, but it works.

Also still missing is a direct redirection to the just fetched entry.
