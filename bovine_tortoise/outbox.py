import asyncio
import logging
import traceback
from datetime import datetime

import aiohttp

import bovine.clients
from bovine.types import LocalUser

from .models import Actor, Follower, OutboxEntry


async def outbox_item_count(local_user: LocalUser) -> int:
    actor = await Actor.get_or_none(account=local_user.name)
    if actor is None:
        print("Failed to fetch actor")
        return 0

    return await OutboxEntry.filter(actor=actor).count()


async def outbox_items(local_user: LocalUser, start: int, limit: int) -> list | None:
    actor = await Actor.get_or_none(account=local_user.name)
    if actor is None:
        print("Failed to fetch actor")
        return None

    result = await OutboxEntry.filter(actor=actor).offset(0).limit(limit).all()

    return [x.content for x in result]


async def send_activity(
    session: aiohttp.ClientSession,
    local_user: LocalUser,
    activity: dict,
    local_path: str,
):
    try:
        actor = await Actor.get_or_none(account=local_user.name)
        if actor is None:
            logging.warn("Failed to fetch actor")
            return

        await OutboxEntry.create(
            actor=actor, created=datetime.now(), content=activity, local_path=local_path
        )

        logging.info(f"Create outbox entry for {local_path}")

        inboxes = []

        # FIXME: Do I need to take into account the audience field?
        # Currently, the audience field is not supported for anything ...
        for account in activity.get("to", []) + activity.get("cc", []):
            if "/followers" in account:
                followers = await Follower.filter(actor=actor).all()
                inboxes += [x.inbox for x in followers]
                logging.info("Adding followers")
            elif "#Public" in account:
                logging.info("Public post")
            else:
                if "mymath.rocks" not in account:
                    logging.info(f"Getting inbox for {account}")
                    inbox = await bovine.clients.get_inbox(session, local_user, account)
                    inboxes.append(inbox)

        inboxes = list(set(inboxes))

        logging.info("Inboxes " + ", ".join(inboxes))

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

        logging.error("Something went wrong when sending activity", ex)
