from bovine.types import LocalUser as LocalUserObject
from tortoise import Tortoise

from .models import Actor
from .outbox import outbox_item_count, outbox_items


async def init(db_url: str = "sqlite://db.sqlite3") -> None:
    await Tortoise.init(
        db_url=db_url,
        modules={"models": ["bovine_tortoise.models"]},
    )
    await Tortoise.generate_schemas()

    return None


default_outbox = (outbox_item_count, outbox_items)


class ManagedDataStore:
    def __init__(
        self,
        db_url="sqlite://db.sqlite3",
        inbox_process=None,
        outbox_handlers=None,
        outbox_process=None,
    ):
        self.db_url = db_url
        self.inbox_process = inbox_process
        self.outbox_process = outbox_process

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
        local_user = local_user.set_inbox_process(
            self.inbox_process
        ).set_outbox_process(self.outbox_process)
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
