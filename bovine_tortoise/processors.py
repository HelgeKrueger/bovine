import traceback
from datetime import datetime

from quart import current_app

import bovine.clients

from bovine.activitystreams.activities import build_accept
from bovine.types import InboxItem, LocalUser

from .models import Actor, InboxEntry, Follower


async def store_in_database(local_user: LocalUser, item: InboxItem) -> InboxItem | None:
    try:
        actor = await Actor.get_or_none(account=local_user.name)

        if actor is None:
            print(f"Actor not found!!! {local_user.name}")
            return item

        await InboxEntry.create(actor=actor, created=datetime.now(), content=item.body)

        return item
    except Exception as ex:
        print(ex)
        traceback.print_exception(type(ex), ex, ex.__traceback__)

        return item


async def accept_follow_request(
    local_user: LocalUser, item: InboxItem
) -> InboxItem | None:
    data = item.get_data()

    if data["type"] != "Follow":
        return item

    try:
        actor = await Actor.get_or_none(account=local_user.name)
        inbox = data["actor"] + "/inbox"

        await Follower.create(
            actor=actor, inbox=inbox, account=data["actor"], followed_on=datetime.now()
        )

        request_data = build_accept(local_user.url, data).build()
        await bovine.clients.send_activitypub_request(
            current_app.config["session"], inbox, request_data, local_user
        )

        return None
    except Exception as ex:
        print(ex)
        traceback.print_exception(type(ex), ex, ex.__traceback__)
        return item


async def store_host_as_peer(
    local_user: LocalUser, item: InboxItem
) -> InboxItem | None:
    # FIXME
    return item
