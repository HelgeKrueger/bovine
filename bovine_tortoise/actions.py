import aiohttp
import json
from datetime import datetime
from urllib.parse import urlparse

from bovine.types import LocalUser
import bovine.clients
from bovine.clients.lookup_account import lookup_account
from bovine.activitystreams.activities import build_follow

from .models import Actor, Following


async def follow(session: aiohttp.ClientSession, local_user: LocalUser, account: str):
    actor = await Actor.get_or_none(account=local_user.name)

    if actor is None:
        print(f"Actor not found !!!! {local_user.name}")
        return

    account_url = await lookup_account(session, account)
    headers = {"Accept": "application/activity+json"}

    print(account_url)

    response = await session.get(account_url, headers=headers, timeout=10)
    text = await response.text()

    data = json.loads(text)

    inbox = data["inbox"]

    await Following.create(actor=actor, account=account_url, followed_on=datetime.now())

    print("created following")

    domain = urlparse(local_user.url).netloc
    activity = build_follow(domain, local_user.url, account_url).build()

    await bovine.clients.send_activitypub_request(inbox, activity, local_user)
