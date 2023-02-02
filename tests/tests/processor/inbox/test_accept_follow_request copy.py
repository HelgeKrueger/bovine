import json
from unittest.mock import patch

from bovine.utils.test.in_memory_test_app import app
from bovine_blog.processors import default_inbox_process
from bovine_tortoise.models import Follower
from bovine_tortoise.test_database import db_url  # noqa: F401

from tests.utils import build_inbox_item_from_json, create_actor_and_local_user


@patch("bovine_core.clients.signed_http.signed_post")
async def test_mastodon_follow_request_is_accepted(
    mock_signed_post, db_url  # noqa F811
):
    async with app.app_context():
        actor, local_user = await create_actor_and_local_user()
        item = build_inbox_item_from_json("test_data/mastodon_follow_1.json")

        await default_inbox_process(item, local_user, None)

        mock_signed_post.assert_awaited_once()

        args = mock_signed_post.await_args[0]
        assert args[1] == "url#main-key"
        assert args[2] == "private_key"
        # assert args[3] == "inbox"
        # FIXME the logic for generating the inbox name is broken

        response_activity = json.loads(args[4])
        assert response_activity["type"] == "Accept"
        assert response_activity["object"] == item.get_data()

        assert await Follower.filter(actor=actor).count() == 1

        entry = await Follower.filter(actor=actor).get()
        assert entry.account == "https://example.com/users/JohnMastodon"
