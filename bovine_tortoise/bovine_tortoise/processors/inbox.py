import logging
import traceback
from datetime import datetime

from bovine.types import LocalActor, ProcessingItem

from bovine_tortoise.models import Actor, InboxEntry

logger = logging.getLogger(__name__)


async def store_in_database(
    item: ProcessingItem, local_user: LocalActor, session
) -> ProcessingItem | None:
    try:
        actor = await Actor.get_or_none(account=local_user.name)

        if actor is None:
            logger.error(f"Actor not found!!! {local_user.name}")
            return item

        content_id = item.get_data().get("id", None)

        obj = item.get_data().get("object", {})
        if isinstance(obj, dict):
            conversation = obj.get("conversation", None)
            object_id = obj.get("id")
            if object_id:
                content_id = object_id
        else:
            conversation = None

        if not content_id:
            logger.warning("Received item without id")

        entry = await InboxEntry.create(
            actor=actor,
            created=datetime.now(),
            content=item.body,
            conversation=conversation,
            content_id=content_id,
        )

        item.meta["database_id"] = entry.id

        return item
    except Exception as ex:
        logger.error(f"{str(ex)} happened when storing into database")
        for log_line in traceback.format_exc().splitlines():
            logger.error(log_line)

        return item


async def inbox_entry_for_id(content_id):
    entry = await InboxEntry.get_or_none(
        content_id=content_id,
    )

    # FIXME: Activities should be stored with the id of the underlying object
    # the following code can probably be removed in a few days ...
    if not entry:
        entry = await InboxEntry.get_or_none(
            content_id=content_id + "/activity",
        )

    return entry


async def remove_from_database(
    item: ProcessingItem, local_user: LocalActor, session
) -> ProcessingItem | None:
    try:
        actor = await Actor.get_or_none(account=local_user.name)

        if actor is None:
            logger.error(f"Actor not found!!! {local_user.name}")
            return

        content_id = determine_content_id(item, for_delete=True)

        if not content_id:
            logger.error("Cannot delete item without id")
            return

        entry = await inbox_entry_for_id(content_id)

        if not entry:
            logger.warning("Item not found")
            return

        await entry.delete()

        logger.info(f"Deleted item with id {content_id}")

        return
    except Exception as ex:
        logger.error(f"{str(ex)} happened when deleting from database")
        for log_line in traceback.format_exc().splitlines():
            logger.error(log_line)

        return


def determine_content_id(item, for_delete=False):
    if isinstance(item, dict):
        data = item
    elif isinstance(item, str):
        return item
    else:
        data = item.get_data()

    if for_delete:
        return data.get("id")

    content_id = data.get("object", {}).get("id")
    if content_id is not None:
        return content_id

    return data.get("id")


async def update_in_database(
    item: ProcessingItem, local_user: LocalActor, session
) -> ProcessingItem | None:
    try:
        actor = await Actor.get_or_none(account=local_user.name)

        if actor is None:
            logger.error(f"Actor not found!!! {local_user.name}")
            return

        content_id = determine_content_id(item)

        if not content_id:
            logger.error("Cannot update item without id")
            return

        entry = await inbox_entry_for_id(content_id)

        if not entry:
            logger.warning(f"Item not found for {content_id}")
            return

        await InboxEntry.filter(content_id=entry.content_id).update(
            content=item.get_data()
        )

        logger.info(f"Updated item with id {content_id}")

        return
    except Exception as ex:
        logger.error(f"{str(ex)} happened when updating from database")
        for log_line in traceback.format_exc().splitlines():
            logger.error(log_line)

        return
