# ActivityPub Client 2 Server

The ReactJS web frontend `buffalo` speaks with the python `bovine` running on a server using a "version" of [client to server activity pub](https://www.w3.org/TR/activitypub/#client-to-server-interactions). At least that is the goal.

## Posting

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

## Reading

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

## Fetching

This is a new endpoint of the form

```
POST https://mymath.rocks/activitypub/helge/fetch
```

which allows one to fetch remote resources. Current support is for fetching an url. This means that I can copy the URL of a post on the Fediverse and reply to it using Buffalo. The current process still involves quite a bit of copy and pasting, but it works.

Also still missing is a direct redirection to the just fetched entry.
