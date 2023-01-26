import asyncio
import json
import random
import uuid

import aiohttp
import cowsay
from markdown import Markdown

from bovine.activitystreams.activities import build_create
from bovine.activitystreams.objects import build_note
from bovine.clients.signed_http import signed_post


def create_note_activity(account_url):
    food_list = [
        "daisies",
        "roses",
        "dandelions",
        "grass",
        "apples",
        "carrots",
        "hay",
        "tulips",
        "turnips",
        "tomatos",
        "pumkins",
        "forget me nots",
        "avocados",
        "christmas trees",
        "the tree of life",
        "yggdrasil",
        "peanuts",
        "soy",
        "cotton",
    ]
    food = random.choice(food_list)

    md = Markdown()
    cow_string = cowsay.get_output_string("cow", f"I'm muniching on {food}.")
    markdown_string = f"""
If the following looks poorly, try opening original post.
Then contact your instance admin, and tell him to support the code tag.


```{cow_string}
```
"""
    payload = md.convert(markdown_string)

    post_url = f"{account_url}/{uuid.uuid4()}"

    note = (
        build_note(account_url, post_url, payload)
        .with_source(markdown_string, "text/markdown")
        .as_public()
        .build()
    )
    return build_create(note).build()


async def post_status(note, public_key_url, private_key, outbox_url):
    body = json.dumps(note)
    async with aiohttp.ClientSession() as session:
        result, status = await signed_post(
            session, public_key_url, private_key, outbox_url, body
        )
        print(result)
        print(status)


account_url = "https://mymath.rocks/activitypub/munchingcow"
public_key_url = f"{account_url}#main-key"
outbox_url = f"{account_url}/outbox"

with open(".files/cow_private.pem", "r") as f:
    private_key = f.read()

note = create_note_activity(account_url)
asyncio.run(post_status(note, public_key_url, private_key, outbox_url))
