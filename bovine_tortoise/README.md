# bovine_tortoise

This provides an extension of bovine based on [tortoise-orm](https://tortoise.github.io/).
In some sense, `bovine` provides an implementation that has no
true storage except dumb everything into log files. With
`bovine_tortoise`, you get a storage backend.

FIXME: Needs a massive rewrite that has been started
in `bovine_store`. `bovine_store` will replace storage
of ActivityPub data, but not the actual management
of server information.
