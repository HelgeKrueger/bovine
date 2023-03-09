# bovine_store

`bovine_store` is meant to be the module handling storing of
local ActivityPub objects and caching of remote ActivityPub
objects.

Some goals and design decisions:

- Objects with an id are stored separately and can be looked up via this id. This is done by json-ld magic.
- Collections are not stored. Instead for local items, the information that the item belongs to a collection is stored. `bovine_store.store.collection` contains the coroutines necessary to build the collection from this information. All collections are assumed to ActivityStreams 2 `OrderedCollection` and ordered by the database id.
- Every object is currently assigned an `owner`. The idea was that an activity is owner by its actor. This can then be propagated to the subobjects, e.g. the object, attachments, and so on. Unfortunately, this is too naive:
  - Some implementations include remote objects, e.g. the object being liked in a Like Activity.
  - Mastodon includes its custom emojis. These have an id and should probably belong to the server.
- There are three kinds of visibility.
  - An object is always visible to its owner
  - Public Objects are assigned `VisibilityType.PUBLIC`. These can viewed by all users providing valid authentication.
  - Furthemore, by adding actors to the `VisibileTo` list of an object. This can be made visible to the corresponding actors.
- An item is visible to be inside a collection if and only if said item is visible. This should probably be augmented by visible to the owner of the collection.
- `bovine_store.blueprint` contains a quart blueprint with the basic retrievel mechanism for the stored objects.
- `bovine_store.collection` contains the helper routine for collection responses.

## Examples

A demonstration webserver can be seen using

```bash
poetry run python examples/create_table.py
poetry run python examples/basic_app.py
```

Note this is a very basic example. Instructions what the example does are
printed to the command line after start.

Note: This example creates two files `db.sqlite3`, which contains the
database and `context_cache.sqlite`, which contains the cache of json-ld
contexts. Furthemore configuration values are read from `bovine_config.toml`.
