import logging
import traceback
from datetime import datetime

from quart import current_app

import bovine.clients
from bovine.activitystreams.activities import build_accept
from bovine.types import InboxItem, LocalUser

from .models import Actor, Follower, InboxEntry, Following

logger = logging.getLogger("tor-proc")


async def store_in_database(item: InboxItem, local_user: LocalUser) -> InboxItem | None:
    try:
        actor = await Actor.get_or_none(account=local_user.name)

        if actor is None:
            logging.error(f"Actor not found!!! {local_user.name}")
            return item

        obj = item.get_data().get("object", {})
        if isinstance(obj, dict):
            conversation = obj.get("conversation", None)
        else:
            conversation = None

        await InboxEntry.create(
            actor=actor,
            created=datetime.now(),
            content=item.body,
            conversation=conversation,
        )

        return item
    except Exception as ex:
        logger.error(f"{str(ex)} happened when storing into database")
        for log_line in traceback.format_exc().splitlines():
            logger.error(log_line)

        return item


async def accept_follow_request(
    item: InboxItem, local_user: LocalUser
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
            current_app.config["session"], local_user, inbox, request_data
        )

        return item
    except Exception as ex:
        print(ex)
        traceback.print_exception(type(ex), ex, ex.__traceback__)
        return item


async def store_host_as_peer(
    item: InboxItem, local_user: LocalUser
) -> InboxItem | None:
    # FIXME
    return item


async def record_accept_follow(
    item: InboxItem, local_user: LocalUser
) -> InboxItem | None:
    try:
        data = item.get_data()

        if data["type"] != "Accept":
            return item

        obj = data["object"]

        if obj["type"] != "Follow":
            return item
            actor = await Actor.get_or_none(account=local_user.name)
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
