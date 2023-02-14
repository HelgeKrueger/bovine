import logging

from bovine.types import LocalActor as LocalActor
from tortoise import Tortoise

from bovine_tortoise.models import Actor, InboxEntry, OutboxEntry

from .utils.count_and_items import CountAndItems

logger = logging.getLogger(__name__)

outbox = CountAndItems(OutboxEntry)
default_outbox = (outbox.item_count, outbox.items)


class ManagedDataStore:
    def __init__(
        self,
        db_url="sqlite://db.sqlite3",
        inbox_process=None,
        outbox_process=None,
    ):
        self.db_url = db_url
        self.inbox_process = inbox_process
        self.outbox_process = outbox_process

    async def connect(self):
        await Tortoise.init(
            db_url=self.db_url, modules={"models": ["bovine_tortoise.models"]}
        )

    async def disconnect(self):
        await Tortoise.close_connections()

    async def get_user(self, username: str) -> LocalActor | None:
        result = await Actor.get_or_none(account=username)
        if not result:
            return None

        local_user = LocalActor(
            result.account,
            result.url,
            result.public_key,
            result.private_key,
            result.actor_type,
        )
        local_user = (
            local_user.set_inbox_process(self.inbox_process)
            .set_outbox_process(self.outbox_process)
            .set_stream("outbox", CountAndItems(OutboxEntry))
            .set_stream("inbox", CountAndItems(InboxEntry))
        )

        return local_user

    async def add_user(self, local_user: LocalActor):
        await Actor.create(
            account=local_user.name,
            url=local_user.url,
            actor_type=local_user.actor_type,
            private_key=local_user.private_key,
            public_key=local_user.public_key,
        )


async def inbox_items_for_actor_from(actor_name, last_database_id):
    actor = await Actor.get_or_none(account=actor_name)
    if not actor:
        logger.warning(f"Lookup for unknown actor name {actor_name}")
        return None

    results = await InboxEntry.filter(actor=actor, id__gt=last_database_id).all()

    return [{"data": x.content, "id": x.id} for x in results]
