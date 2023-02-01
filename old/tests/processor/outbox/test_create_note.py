from unittest.mock import patch
import aiohttp

from bovine_tortoise.processors import default_outbox_process
from bovine_tortoise.test_database import db_url  # noqa: F401
from bovine_tortoise.models import OutboxEntry

from tests.utils import create_actor_and_local_user, get_activity_from_json


@patch("bovine_core.clients.signed_http.signed_post")
async def test_buffalo_create_note(mock_signed_post, db_url):  # noqa F811
    async with aiohttp.ClientSession() as session:
        actor, local_user = await create_actor_and_local_user()

        item = get_activity_from_json("test_data/buffalo_create_note_1.json")

        await default_outbox_process(item, local_user, session)

        assert await OutboxEntry.filter(actor=actor).count() == 1

        entry = await OutboxEntry.filter(actor=actor).get()

        assert entry.content == item
