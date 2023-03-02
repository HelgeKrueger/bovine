from .content.handle_update import handle_update
from .content.incoming_delete import incoming_delete
from .content.store_incoming import store_incoming
from .undo import undo

default_content_processors = {
    "Create": store_incoming,
    "Update": handle_update,
    "Delete": incoming_delete,
    "Undo": undo,
}
