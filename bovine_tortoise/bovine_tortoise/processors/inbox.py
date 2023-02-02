import logging
import traceback
from datetime import datetime

import bovine.clients
from bovine.types import InboxItem, LocalUser
from bovine_core.activitystreams.activities import build_accept
from quart import current_app

from bovine_tortoise.models import Actor, Follower, Following, InboxEntry

logger = logging.getLogger("tor-proc")


async def store_in_database(item: InboxItem, local_user: LocalUser) -> InboxItem | None:
    try:
        actor = await Actor.get_or_none(account=local_user.name)

        if actor is None:
            logger.error(f"Actor not found!!! {local_user.name}")
            return item

        obj = item.get_data().get("object", {})
        if isinstance(obj, dict):
            conversation = obj.get("conversation", None)
        else:
            conversation = None

        content_id = item.get_data().get("id", None)

        if not content_id:
            logger.warning("Received item without id")

        await InboxEntry.create(
            actor=actor,
            created=datetime.now(),
            content=item.body,
            conversation=conversation,
            content_id=content_id,
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

        # FIXME: This is broken
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


async def remove_from_database(
    item: InboxItem, local_user: LocalUser
) -> InboxItem | None:
    try:
        actor = await Actor.get_or_none(account=local_user.name)

        if actor is None:
            logger.error(f"Actor not found!!! {local_user.name}")
            return item

        if isinstance(item, dict):
            content_id = item["id"]
        else:
            content_id = item.get_data().get("id", None)

        if not content_id:
            logger.error("Cannot delete item without id")
            return item

        entry = await InboxEntry.get_or_none(
            content_id=content_id,
        )

        if not entry:
            logger.warning("Item not found")
            return item

        await entry.delete()

        logger.info(f"Deleted item with id {content_id}")

        return
    except Exception as ex:
        logger.error(f"{str(ex)} happened when storing into database")
        for log_line in traceback.format_exc().splitlines():
            logger.error(log_line)

        return item
