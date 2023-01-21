from tortoise import Tortoise

from bovine.types import LocalUser as LocalUserObject
from .models import Actor
from .processors import store_in_database, accept_follow_request
from .outbox import outbox_item_count, outbox_items


async def init(db_url: str = "sqlite://db.sqlite3") -> None:
    await Tortoise.init(
        db_url=db_url,
        modules={"models": ["bovine_tortoise.models"]},
    )
    await Tortoise.generate_schemas()

    return None


default_inbox_processors = [
    accept_follow_request,
    store_in_database,
]
default_outbox = (outbox_item_count, outbox_items)


class ManagedDataStore:
    def __init__(
        self, db_url="sqlite://db.sqlite3", inbox_processors=[], outbox_handlers=None
    ):
        self.db_url = db_url
        self.inbox_processors = inbox_processors
        self.outbox_handlers = outbox_handlers

    async def connect(self):
        await Tortoise.init(
            db_url=self.db_url, modules={"models": ["bovine_tortoise.models"]}
        )

    async def disconnect(self):
        await Tortoise.close_connections()

    async def get_user(self, username: str) -> LocalUserObject | None:
        result = await Actor.get_or_none(account=username)
        if not result:
            return None

        local_user = LocalUserObject(
            result.account,
            result.url,
            result.public_key,
            result.private_key,
            result.actor_type,
        )
        for p in self.inbox_processors:
            local_user = local_user.add_inbox_processor(p)

        if self.outbox_handlers:
            local_user = local_user.set_outbox(*self.outbox_handlers)

        return local_user

    async def add_user(self, local_user: LocalUserObject):
        await Actor.create(
            account=local_user.name,
            url=local_user.url,
            actor_type=local_user.actor_type,
            private_key=local_user.private_key,
            public_key=local_user.public_key,
        )
