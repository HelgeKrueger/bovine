from bovine.utils.test.in_memory_test_app import app
from bovine_blog.processors import default_inbox_process
from bovine_tortoise.test_database import db_url  # noqa: F401

from tests.utils import build_inbox_item_from_json, create_actor_and_local_user


async def test_mastodon_delete_actor(db_url):  # noqa F811
    async with app.app_context():
        actor, local_user = await create_actor_and_local_user()
        like_item = build_inbox_item_from_json("data/mastodon_delete_actor_1.json")

        await default_inbox_process(like_item, local_user, None)
