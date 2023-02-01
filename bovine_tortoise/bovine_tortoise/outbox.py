import logging

from bovine.types import LocalUser

from .models import Actor, OutboxEntry

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
