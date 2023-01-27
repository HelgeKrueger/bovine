import asyncio
import logging
import traceback
from datetime import datetime

import aiohttp

import bovine.clients
from bovine.types import LocalUser

from .models import Actor, Follower, OutboxEntry


logger = logging.getLogger("outbox")


async def outbox_item_count(local_user: LocalUser) -> int:
    actor = await Actor.get_or_none(account=local_user.name)
    if actor is None:
        logger.error("Failed to fetch actor")
        return 0

    return await OutboxEntry.filter(actor=actor).count()


async def outbox_items(local_user: LocalUser, start: int, limit: int) -> list | None:
    actor = await Actor.get_or_none(account=local_user.name)
    if actor is None:
        logger.error("Failed to fetch actor")
        return None

    result = await OutboxEntry.filter(actor=actor).offset(0).limit(limit).all()

    return [x.content for x in result]


async def send_activity_no_local_path(
    local_user: LocalUser, session: aiohttp.ClientSession, activity: dict
):
    local_path = "/".join(activity["id"].split("/")[-2:])
    return await send_activity(session, local_user, activity, local_path)


async def send_activity(
    session: aiohttp.ClientSession,
    local_user: LocalUser,
    activity: dict,
    local_path: str,
):
    try:
        actor = await Actor.get_or_none(account=local_user.name)
        if actor is None:
            logger.warn("Failed to fetch actor")
            return

        await OutboxEntry.create(
            actor=actor, created=datetime.now(), content=activity, local_path=local_path
        )

        logger.info(f"Create outbox entry for {local_path}")

        inboxes = []

        # FIXME: Do I need to take into account the audience field?
        # Currently, the audience field is not supported for anything ...
        for account in activity.get("to", []) + activity.get("cc", []):
            if "/followers" in account:
                followers = await Follower.filter(actor=actor).all()
                inboxes += [x.inbox for x in followers]
                logger.info("Adding followers")
            elif "#Public" in account:
                logger.info("Public post")
            else:
                if "mymath.rocks" not in account:
                    logger.info(f"Getting inbox for {account}")
                    inbox = await bovine.clients.get_inbox(session, local_user, account)
                    inboxes.append(inbox)

        inboxes = list(set(inboxes))

        logger.info("Inboxes " + ", ".join(inboxes))

        await asyncio.gather(
            *[
                bovine.clients.send_activitypub_request(
                    session, local_user, inbox, activity
                )
                for inbox in inboxes
            ]
        )
    except Exception as ex:
        traceback.print_exception(type(ex), ex, ex.__traceback__)

        logger.error("Something went wrong when sending activity", ex)
