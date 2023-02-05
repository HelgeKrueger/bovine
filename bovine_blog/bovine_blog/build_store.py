from bovine import get_bovine_user
from bovine.utils.in_memory_store import InMemoryUserStore
from bovine_tortoise import ManagedDataStore

from .processors import default_inbox_process, default_outbox_process


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
        inbox_process=default_inbox_process,
        outbox_process=default_outbox_process,
    )

    return bovine_user, Chain(bovine_store.get_user, data_store.get_user).execute
