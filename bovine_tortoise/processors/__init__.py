from .inbox import accept_follow_request, store_in_database, record_accept_follow
from .outbox import send_activity_no_local_path, create_outbox_entry

default_inbox_processors = [
    accept_follow_request,
    store_in_database,
    record_accept_follow,
]

default_outbox_processors = [create_outbox_entry, send_activity_no_local_path]
