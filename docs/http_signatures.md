# HTTP Signatures

Bovine implements HTTP Signatures to the best of my abilities. For background see the [Mastodon documentation](https://docs.joinmastodon.org/spec/security/#http). My basic premise when implementing bovine was to be as strict as possible, and then relax if necessary. So bovine behaves like Mastodon with [AUTHORIZED_FETCH=True](https://docs.joinmastodon.org/admin/config/#authorized_fetch).

**FIXME**: Bovine currently only supports the `rsa-sha256` algorithm for HTTP Signatures. An algorithm called `hs2019` is also used, but much less, it should be supported for signature checking.

## Application user: bovine

HTTP signatures reference a public key through the keyId property, e.g.

```
keyId="https://mymath.rocks/activitypub/bovine#main-key"
```

This means that if all requests between servers were to be signed, we would run into a chicken-and-egg problem.

To avoid this problem, bovine uses an application user with name bovine, whose initial profile is public. Fetches for public keys are done using this application user.

## Implementation of signature checking

Currently, the HTTP signature is checked with the `@before_request` function defined in `bovine.server.rewrite_request`. This function has also the task to redirect all non activitypub traffic, i.e. not having the type `application/activity+json` or equivalent, to the text based outputs.

Actually, checking that proper authorization for the endpoint is available is done on an individual endpoint basis. This done so that for

```
POST /activitypub/<user>/outbox
GET /activitypub/<user>/inbox
```

only the public key associated with `user` is valid. For other endpoints any signature is valid.

### Public Key Fetching

The method used to validate signatures is currently stored in

```
app.config["validate_signature"]
```

This is done in order to be able to use a public key cache provided by `bovine_tortoise.caches.build_public_key_fetcher`.

**FIXME**: Why not just store the public key fetcher?

## Fetching and Posting with signatures

The methods `signed_get` and `signed_post` implement the standard HTTP methods while adding appropriate signatures. They can be found in `bovine.clients.signed_http`.
