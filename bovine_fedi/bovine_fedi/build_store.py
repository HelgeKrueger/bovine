from bovine_user.types import EndpointType
from quart import current_app

from bovine_fedi.types import LocalActor
from bovine_fedi.utils import get_bovine_user
from bovine_fedi.utils.in_memory_store import InMemoryUserStore


class Chain:
    def __init__(self, *coroutines):
        self.coroutines = coroutines

    async def execute(self, username):
        for coro in self.coroutines:
            result = await coro(username)
            if result is not None:
                return result

        return None


async def get_user_from_bovine_user_manager(name):
    manager = current_app.config["bovine_user_manager"]

    user = await manager.get_user_for_name(name)

    if user is None:
        return

    endpoints = [x for x in user.endpoints if x.endpoint_type == EndpointType.ACTOR]
    keypair = user.keypairs[0]

    return LocalActor(
        user.handle_name,
        endpoints[0].name,
        keypair.public_key,
        keypair.private_key,
        "Tombstone",
    )


def build_get_user(domain: str):
    bovine_user = get_bovine_user(domain)

    bovine_store = InMemoryUserStore()
    bovine_store.add_user(bovine_user)

    return (
        bovine_user,
        Chain(
            bovine_store.get_user,
            get_user_from_bovine_user_manager,
        ).execute,
    )
