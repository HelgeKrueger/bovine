from bovine import get_bovine_user
from bovine.utils.in_memory_store import InMemoryUserStore
from bovine_tortoise import ManagedDataStore, default_outbox
from bovine_tortoise.processors import (
    default_inbox_processors,
    default_outbox_processors,
)


class Chain:
    def __init__(self, *coroutines):
        self.coroutines = coroutines

    async def execute(self, username):
        for coro in self.coroutines:
            result = await coro(username)
            if result is not None:
                return result

        return None


def build_get_user(domain: str):
    bovine_user = get_bovine_user(domain)

    bovine_store = InMemoryUserStore()
    bovine_store.add_user(bovine_user)

    data_store = ManagedDataStore(
        inbox_processors=default_inbox_processors,
        outbox_handlers=default_outbox,
        outbox_processors=default_outbox_processors,
    )

    return bovine_user, Chain(bovine_store.get_user, data_store.get_user).execute
