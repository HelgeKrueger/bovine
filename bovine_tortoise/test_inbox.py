from datetime import datetime

from .models import Actor, InboxEntry
from .inbox import inbox_content_starting_from
from .test_database import db_url  # noqa: F401


async def test_basic_inbox(db_url):  # noqa: F811
    actor = await Actor.create(
        account="name",
        url="url",
        actor_type="type",
        private_key="private_key",
        public_key="public_key",
    )
    await InboxEntry.create(actor=actor, created=datetime.now(), content={"a": "b"})

    result = await inbox_content_starting_from("name", 0)

    assert len(result) == 1
