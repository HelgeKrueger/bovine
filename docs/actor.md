# Actor

The endpoint describing an actor, e.g. `https://mymath.rocks/activitypub/bovine` returns

```
{
    "@context": [
        "https://www.w3.org/ns/activitystreams",
        "https://w3id.org/security/v1"
    ],
    "id": "https://mymath.rocks/activitypub/bovine",
    "inbox": "https://mymath.rocks/activitypub/bovine/inbox",
    "name": "bovine",
    "outbox": "https://mymath.rocks/activitypub/bovine/outbox",
    "preferredUsername": "bovine",
    "publicKey": {
        "id": "https://mymath.rocks/activitypub/bovine#main-key",
        "owner": "https://mymath.rocks/activitypub/bovine",
        "publicKeyPem": "-----BEGIN PUBLIC KEY-----....-----END PUBLIC KEY-----\n"
    },
    "type": "Application"
}
```

Two comments on this:

- `publicKey` is required see [HTTP Signatures](http_signatures.md)
- `preferredUsername` is required to interact with Mastodon. The reason is explained below

## PreferredUsername and Mastodon

Mastodon doesn't seem to identify actors with their url, e.g. `https://mymath.rocks/activitypub/bovine`,
instead it identifies them with their "username", e.g. `bovine@mymath.rocks`. This means that
when looking up `bovine@mymath.rocks` on Mastodon the following requests happen:

```
GET /.well-known/webfinger?resource=acct:bovine@mymath.rocks
GET /activitypub/bovine
GET /.well-known/webfinger?resource=acct:$PREFERRED_USERNAME@mymath.rocks
...
```

This means that in order to interact with Mastodon, you need both the webfinger endpoint
and specify the `preferredUsername` property in the actor object. Neither is
required by ActivityPub as far as I can tell.
