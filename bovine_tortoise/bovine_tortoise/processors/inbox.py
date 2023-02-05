import logging
import traceback
from datetime import datetime

from bovine.types import LocalActor, ProcessingItem

from bovine_tortoise.models import Actor, InboxEntry

logger = logging.getLogger("tor-proc")


async def store_in_database(
    item: ProcessingItem, local_user: LocalActor, session
) -> ProcessingItem | None:
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


async def remove_from_database(
    item: ProcessingItem, local_user: LocalActor, session
) -> ProcessingItem | None:
    try:
        actor = await Actor.get_or_none(account=local_user.name)

        if actor is None:
            logger.error(f"Actor not found!!! {local_user.name}")
            return

        if isinstance(item, dict):
            content_id = item["id"]
        else:
            content_id = item.get_data().get("id", None)

        if not content_id:
            logger.error("Cannot delete item without id")
            return

        entry = await InboxEntry.get_or_none(
            content_id=content_id,
        )

        if not entry:
            logger.warning("Item not found")
            return

        await entry.delete()

        logger.info(f"Deleted item with id {content_id}")

        return
    except Exception as ex:
        logger.error(f"{str(ex)} happened when storing into database")
        for log_line in traceback.format_exc().splitlines():
            logger.error(log_line)

        return
