import json
from unittest.mock import patch

from bovine.utils.test.in_memory_test_app import app
from bovine_blog.processors import default_inbox_process
from bovine_tortoise.models import InboxEntry
from bovine_tortoise.test_database import db_url  # noqa: F401

from tests.utils import build_inbox_item_from_json, create_actor_and_local_user


@patch("bovine_core.clients.signed_http.signed_post")
async def test_mastodon_like_then_undo(mock_signed_post, db_url):  # noqa F811
    async with app.app_context():
        actor, local_user = await create_actor_and_local_user()
        like_item = build_inbox_item_from_json("test_data/mastodon_like_1.json")
        undo_item = build_inbox_item_from_json("test_data/mastodon_like_1_undo.json")

        like_item_id = like_item.get_data()["id"]

        await default_inbox_process(like_item, local_user, None)
        assert await InboxEntry.filter(actor=actor).count() == 1

        inbox_entry = await InboxEntry.filter(actor=actor).get()

        assert inbox_entry.content_id == like_item_id

        await default_inbox_process(undo_item, local_user, None)

        assert await InboxEntry.filter(actor=actor).count() == 0
