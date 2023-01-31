import logging

from bovine.processors import build_do_for_types
from bovine.processors.dismiss_delete import dismiss_delete
from bovine.processors.processor_list import ProcessorList
from bovine.types import InboxItem, LocalUser

from .inbox import accept_follow_request, record_accept_follow, store_in_database
from .outbox import (
    create_outbox_entry,
    send_activity_no_local_path,
    delete_outbox_entry,
)

logger = logging.getLogger("proc")


async def on_delete(
    local_user: LocalUser,
    item: InboxItem,
):
    logger.warning(f"Delete happened of {item.get_body_id()}")
    logger.info(item.body)


default_inbox_process = (
    ProcessorList()
    .add(
        build_do_for_types(
            {
                "Accept": record_accept_follow,
                "Delete": dismiss_delete(on_delete),
                "Follow": accept_follow_request,
            }
        )
    )
    .add(store_in_database)
    .apply
)


default_outbox_process = (
    ProcessorList()
    .add(
        build_do_for_types(
            {
                "Add": create_outbox_entry,
                "Announce": create_outbox_entry,
                "Create": create_outbox_entry,
                "Update": create_outbox_entry,
                "Delete": delete_outbox_entry,
            }
        )
    )
    .add(
        send_activity_no_local_path,
    )
    .apply
)
