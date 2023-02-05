import logging
import traceback
from datetime import datetime

import bovine.clients
from bovine.types import LocalActor, ProcessingItem
from bovine_core.activitystreams.activities import build_accept

from bovine_tortoise.models import Actor, Follower, Following

logger = logging.getLogger("tor-proc")


async def accept_follow_request(
    item: ProcessingItem, local_user: LocalActor, session
) -> ProcessingItem | None:
    data = item.get_data()

    if data["type"] != "Follow":
        return item

    try:
        actor = await Actor.get_or_none(account=local_user.name)

        # FIXME: This is broken
        inbox = data["actor"] + "/inbox"

        await Follower.create(
            actor=actor, inbox=inbox, account=data["actor"], followed_on=datetime.now()
        )

        request_data = build_accept(local_user.url, data).build()
        await bovine.clients.send_activitypub_request(
            session, local_user, inbox, request_data
        )

        return item
    except Exception as ex:
        print(ex)
        traceback.print_exception(type(ex), ex, ex.__traceback__)
        return item


async def store_host_as_peer(
    item: ProcessingItem, local_user: LocalActor
) -> ProcessingItem | None:
    # FIXME
    return item


async def record_accept_follow(
    item: ProcessingItem, local_user: LocalActor, session
) -> ProcessingItem | None:
    try:
        data = item.get_data()

        if data["type"] != "Accept":
            return item

        obj = data["object"]

        if obj["type"] != "Follow":
            return item

        actor = await Actor.get_or_none(account=local_user.name)
        if actor is None:
            logging.error(f"Actor not found!!! {local_user.name}")
            return item

        await Following.create(
            actor=actor, account=data["actor"], followed_on=datetime.now()
        )

    except Exception as ex:
        logger.error("Something went wrong when recording accept follow")
        logger.error(ex)
        traceback.print_exception(type(ex), ex, ex.__traceback__)
        return item

    return item
