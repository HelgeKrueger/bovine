from datetime import datetime

from bovine_tortoise.models import Actor, OutboxEntry
from bovine_tortoise.utils import db_url  # noqa F401

from .types import PostEntry


def test_post_entry_build_link():
    post_entry = PostEntry("local_id", "author", datetime.now(), "content")

    assert post_entry.build_link() == "/author/local_id"


def test_post_entry_build_published():
    published = datetime(2000, 10, 20, 0, 0, 0)
    post_entry = PostEntry("local_id", "author", published, "content")

    assert post_entry.build_published() == "2000-10-20 00:00:00"


async def test_post_entry_from_outbox_entry(db_url):  # noqa F811
    actor = await Actor.create(
        account="name",
        url="proto://url",
        actor_type="Person",
        public_key="",
        private_key="",
    )

    data = {"object": {"inReplyTo": "author", "content": "blabla"}}

    outbox_entry = await OutboxEntry.create(
        actor=actor, local_path="me/path", created=datetime.now(), content=data
    )

    post_entry = PostEntry.from_outbox_entry(outbox_entry)

    assert post_entry.in_reply_to == "author"
    assert post_entry.author == "me"
    assert post_entry.local_id == "path"
