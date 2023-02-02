from unittest.mock import patch

import aiohttp
from bovine_blog.processors import default_outbox_process
from bovine_tortoise.models import OutboxEntry
from bovine_tortoise.test_database import db_url  # noqa: F401

from tests.utils import create_actor_and_local_user, get_activity_from_json


@patch("bovine_core.clients.signed_http.signed_post")
async def test_create_then_delete(mock_signed_post, db_url):  # noqa F811
    async with aiohttp.ClientSession() as session:
        actor, local_user = await create_actor_and_local_user()
        create = get_activity_from_json("test_data/munching_cow_create_note_1.json")
        delete = get_activity_from_json("test_data/munching_cow_delete_1.json")

        await default_outbox_process(create, local_user, session)

        assert await OutboxEntry.filter(actor=actor).count() == 1
        entry = await OutboxEntry.filter(actor=actor).get()
        assert entry.content == create
        assert entry.local_path == "munchingcow/9c1d3b44-c6f6-4310-9113-a0c3d3208cac"

        await default_outbox_process(delete, local_user, session)

        assert await OutboxEntry.filter(actor=actor).count() == 0
