import logging


from bovine.processors.dismiss_delete import dismiss_delete
from bovine_tortoise import (
    ManagedDataStore,
    default_inbox_processors,
    default_outbox,
)
from bovine import get_bovine_user
from bovine.stores.in_memory import InMemoryUserStore


async def on_delete(local_user, item):
    logging.warning(f"Delete happened of {item.get_body_id()}")
    # item.dump()


class Chain:
    def __init__(self, *coroutines):
        self.coroutines = coroutines

    async def execute(self, username):
        for coro in self.coroutines:
            result = await coro(username)
            if result is not None:
                return result

        return None


def build_get_user(domain):
    bovine_user = get_bovine_user(domain)

    bovine_store = InMemoryUserStore()
    bovine_store.add_user(bovine_user)

    inbox_processors = [dismiss_delete(on_delete)] + default_inbox_processors
    data_store = ManagedDataStore(
        inbox_processors=inbox_processors, outbox_handlers=default_outbox
    )

    return bovine_user, Chain(bovine_store.get_user, data_store.get_user).execute
