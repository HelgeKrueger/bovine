import asyncio
import logging
import traceback
from datetime import datetime

import aiohttp

import bovine.clients
from bovine.types import LocalUser
from bovine_tortoise.models import Actor, Follower, OutboxEntry

logger = logging.getLogger("outbox-proc")


# FIXME this is horrible
def determine_local_path_from_activity_id(activity_id):
    local_path = activity_id
    local_path = local_path.removesuffix("/activity")
    local_path = "/".join(local_path.split("/")[-2:])
    return local_path


async def create_outbox_entry(
    activity: dict,
    local_user: LocalUser,
    session: aiohttp.ClientSession,
):
    local_path = determine_local_path_from_activity_id(activity["id"])
    actor = await Actor.get_or_none(account=local_user.name)
    if actor is None:
        logger.warn("Failed to fetch actor")
        return

    await OutboxEntry.create(
        actor=actor, created=datetime.now(), content=activity, local_path=local_path
    )

    logger.info(f"Created outbox entry for {local_path}")

    return activity


async def send_activity_no_local_path(
    activity: dict,
    local_user: LocalUser,
    session: aiohttp.ClientSession,
):

    local_path = determine_local_path_from_activity_id(activity["id"])
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
                # FIXME this is horrible
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
