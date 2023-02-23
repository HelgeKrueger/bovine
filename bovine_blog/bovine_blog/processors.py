import json

from bovine.processors.fetch_object_and_process import fetch_object_and_process
from bovine.processors.inbox.add_to_queue import add_to_queue
from bovine.processors.outbox.replace_ids import replace_ids
from bovine.processors.processor_list import ProcessorList
from bovine.types import LocalActor, ProcessingItem
from bovine_store.processors import default_content_processors
from bovine_store.processors.content.store_incoming import (
    add_incoming_to_inbox,
    store_incoming,
)

# from bovine_tortoise.processors.inbox import (
#     remove_from_database,
#     store_in_database,
#     update_in_database,
# )
from bovine_tortoise.processors.inbox_follow import (
    accept_follow_request,
    record_accept_follow,
)
from bovine_tortoise.processors.outbox import (
    create_outbox_entry,
    delete_outbox_entry,
    send_activity_no_local_path,
)
from markdown import Markdown

default_inbox_process = (
    ProcessorList()
    .add_for_types(
        **default_content_processors,
        Accept=record_accept_follow,
        Announce=fetch_object_and_process,
        # Update=update_in_database,
        # Delete=incoming_delete,
        # Delete=ProcessorList(on_object=True).add(remove_from_database).apply,
        Follow=accept_follow_request,
        # Undo=ProcessorList(on_object=True)
        # .add_for_types(Like=remove_from_inbox, Announce=remove_from_inbox)
        # .apply,
    )
    # .add(store_in_database)
    .add(store_incoming)
    .add(add_incoming_to_inbox)
    .add(add_to_queue)
    .apply
)


async def fix_markup(item: ProcessingItem, local_actor: LocalActor):
    if isinstance(item, dict):
        obj = item
    else:
        obj = item.get_data()

    if "object" in obj and "id" in obj["object"]:
        md = Markdown(extensions=["mdx_math"])

        if "source" in obj["object"]:
            obj["object"]["content"] = md.convert(obj["object"]["source"]["content"])
            if "contentMap" in obj["object"]:
                obj["object"]["contentMap"]["en"] = md.convert(
                    obj["object"]["source"]["content"]
                )

    if isinstance(item, dict):
        return item

    item.data = obj
    item.body = json.dumps(obj)

    return item


default_outbox_process = (
    ProcessorList()
    .add(fix_markup)
    .add_for_types(
        Create=replace_ids,
    )
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
