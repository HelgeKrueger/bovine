from typing import List

from bovine_tortoise.models import Actor, OutboxEntry

from .types import PostEntry


class TortoiseStore:
    def __init__(self, username="helge"):
        self.username = username

    async def index_contents(self) -> List[PostEntry]:
        entries = await OutboxEntry.filter().order_by("-created").limit(10).all()

        contents = [PostEntry.from_outbox_entry(entry).as_dict() for entry in entries]

        return contents

    async def user_contents(self, username) -> List[PostEntry]:
        actor = await Actor.get_or_none(account=username)
        entries = (
            await OutboxEntry.filter(actor=actor).order_by("-created").limit(10).all()
        )

        contents = [PostEntry.from_outbox_entry(entry).as_dict() for entry in entries]

        return contents

    async def user_post(self, username: str, uuid: str) -> PostEntry | None:
        actor = await Actor.get_or_none(account=username)

        if actor is None:
            return None

        local_path = f"{username}/{uuid}"

        entry = await OutboxEntry.get_or_none(actor=actor, local_path=local_path)

        if entry is None:
            return None

        return PostEntry.from_outbox_entry(entry).as_dict()
