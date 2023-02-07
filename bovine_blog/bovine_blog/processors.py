# import logging

# from bovine.processors.dismiss_delete import dismiss_delete
from bovine.processors.fetch_object_and_process import fetch_object_and_process
from bovine.processors.processor_list import ProcessorList

# from bovine.types import LocalActor, ProcessingItem
from bovine_tortoise.processors.inbox import remove_from_database, store_in_database
from bovine_tortoise.processors.inbox_follow import (
    accept_follow_request,
    record_accept_follow,
)
from bovine_tortoise.processors.outbox import (
    create_outbox_entry,
    delete_outbox_entry,
    send_activity_no_local_path,
)

# logger = logging.getLogger(__name__)


# async def on_delete(local_user: LocalActor, item: ProcessingItem, session):
#     logger.warning(f"Delete happened of {item.get_body_id()}")
#     logger.debug(item.body)


default_inbox_process = (
    ProcessorList()
    .add_for_types(
        Accept=record_accept_follow,
        Announce=fetch_object_and_process,
        Delete=ProcessorList(on_object=True).add(remove_from_database).apply,
        Follow=accept_follow_request,
        Undo=ProcessorList(on_object=True)
        .add_for_types(Like=remove_from_database, Announce=remove_from_database)
        .apply,
    )
    .add(store_in_database)
    .apply
)


default_outbox_process = (
    ProcessorList()
    .add_for_types(
        Add=create_outbox_entry,
        Announce=create_outbox_entry,
        Create=create_outbox_entry,
        Update=create_outbox_entry,
        Delete=delete_outbox_entry,
    )
    .add(
        send_activity_no_local_path,
    )
    .apply
)
