# Bovine powered RSS to ActivityPub

Sample project to create a [bovine](https://github.com/HelgeKrueger/bovine) that
takes an RSS feed and converts it to ActivityPub.

_Note_: Resisa needs Python 3.11 as `asyncio.TaskGroup` is being used.

## Generating keys and creating a user in bovine_blog

For other platforms that allow authentication through HTTP Signatures, follow their
instruction to obtain a user and their private key.

Generate public and private keys

```
python generate_keys.py
```

This creates the files `private_key.pem` and `public_key.pem`. Uploads these to
your bovine or similar installed activitypub server and use these to create
a new user. For `bovine_blog` the following works

```
DOMAIN=$MY_DOMAIN poetry run python bovine_blog/scripts/add_user.py wordoftheday_merriamwebster --public_key $PUBLIC_KEY --private_key $PRIVATE_KEY
```

## Configuration

Configuration is done via a config file `resisa.toml`. It's format is:

```
[merriam_webster_word_of_the_day]

feed_url = "https://www.merriam-webster.com/wotd/feed/rss2"
account_url = "https://mymath.rocks/activitypub/wordoftheday_merriamwebster"
outbox_url = "https://mymath.rocks/activitypub/wordoftheday_merriamwebster/outbox"
public_key_url = "https://mymath.rocks/activitypub/wordoftheday_merriamwebster#main-key"
private_key = """
-----BEGIN PRIVATE KEY-----
....
-----END PRIVATE KEY-----
"""
```

**Note**: Multiple entries are possible. Those are processed sequentially.

## Running

Once it is done `resisa` can be run via

```
poetry run python resisa.py
```

Resisa ensures that the entries in the activitypub outbox match those in the RSS feed.
