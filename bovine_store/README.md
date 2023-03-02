# bovine_store

`bovine_store` is meant to be the module handling storing of
local ActivityPub objects and caching of remote ActivityPub
objects.

The goal is two fold:

- Handle visibility and ability to update content
- Simplify working with json-ld

## Examples

A basic example is contained in `examples/basic_app.py`. Note
this is a very basic example.

## Permissions

Permissions, i.e. who can view what, are a messy subject.
The simplest version is that an actor can only view, what
gets delivered to its inbox. This is broken by the use
of shared inboxes, fetching remote data, and so on. So one
needs a model for this. I will try to implement the following
principles:

- Extract actors from the to, cc, bto, bcc fields
- Extract collections from these fields
- Check if public

### Access

- A remote actor can only access objects owned by this store.
- Any valid actor can access a public object
- A named actor can access objects, he is named for

Collections are resolved on storage of remote objects.

## Data fetching

Remote content is fetched using appropriate means.

## JSON-LD

json-ld is a mess to store. This implementation will simplify stuff. Generally, objects with an id are stored
separately.
