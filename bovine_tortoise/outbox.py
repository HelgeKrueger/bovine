import asyncio
from datetime import datetime
import logging
import traceback

from bovine.types import LocalUser
import bovine.clients

from .models import OutboxEntry, Actor, Follower


async def outbox_item_count(local_user: LocalUser) -> int:
    actor = await Actor.get_or_none(account=local_user.name)
    if actor is None:
        print("Failed to fetch actor")
        return 0

    return await OutboxEntry.filter(actor=actor).count()


async def outbox_items(local_user: LocalUser, start: int, limit: int) -> list:
    actor = await Actor.get_or_none(account=local_user.name)
    if actor is None:
        print("Failed to fetch actor")
        return 0

    result = await OutboxEntry.filter(actor=actor).offset(0).limit(limit).all()

    return [x.content for x in result]


async def send_activity(local_user: LocalUser, activity: dict, local_path: str) -> None:
    try:
        actor = await Actor.get_or_none(account=local_user.name)
        if actor is None:
            logging.warn("Failed to fetch actor")
            return 0

        await OutboxEntry.create(
            actor=actor, created=datetime.now(), content=activity, local_path=local_path
        )

        logging.info(f"Create outbox entry for {local_path}")

        followers = await Follower.filter(actor=actor).all()
        inboxes = [x.inbox for x in followers]

        await asyncio.gather(
            *[
                bovine.clients.send_activitypub_request(inbox, activity, local_user)
                for inbox in inboxes
            ]
        )
    except Exception as ex:
        print(ex)
        traceback.print_exception(type(ex), ex, ex.__traceback__)

        logging.error("Something went wrong when sending activity")
