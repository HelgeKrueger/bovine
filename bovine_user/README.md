# bovine_user

`bovine_user` is my attempt at creating a user management system for bovine. The workflow is pretty simple:

- [Hellō](https://www.hello.coop/index.html) will be used to provide authentication and initial authorization.
- The user gets to enter a Fediverse username. This value is used as the `preferredUsername` for the ActivityPub actor and in the Fediverse handle, which is of the form `preferredUsernam@domain`. This step is necessary to be compatible with Mastodon.
- A name can be set in the database table corresponding to `BovineUserProperty`. This can be extended to store more properties, such as summary but has not yet. Some form of administration of these values is necessary.
- In the table `BovineUserEndpoint` the various endpoints for the actor are defined (e.g. actor, inbox, outbox, ...)
- A public, private key pair is generated for the user and stored in `BovineUserKeyPair`.

As with the rest of the bovine project configuration is read from `bovine_config.toml` in the coroutine `bovine_user.config.configure_bovine_user`. Notable values are `bovine.secret_key` which is used by `quart_auth` to handle cookies and `bovine_user.hello_client_id` which comes from registring an application at [Hellō.dev](https://console.hello.coop/).

There are two entrypoints used from outside `bovine_user`. The first is `bovine_user.server` which contains a quart Blueprint called `server`, which defines the necessary authentication and user managemenet methods. Second the configuration routine creates the variable `app.config["bovine_user_manager"]`. This manager is used to both resolve the endpoints defined via `BovineUserEndpoint` as to get the user information via `get_activity_pub`.

## Development

As the entire bovine project there are tests with pytest. Code is formatted via black and linted with flake8. Finally, by running

```bash
poetry run python examples/create_table.py
poetry run python examples/basic_app.py
```

one can start a simple application that exposes the endpoints configured in `bovine_user.server`.

As the functionality of this package does not relate to ActivityPub and general federation most of it is not covered by the tests in `tests/`.
