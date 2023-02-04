import asyncio
import json

from tests.utils import fake_post_headers, get_activity_from_json
from tests.utils.blog_test_env import (  # noqa: F401
    blog_test_env,
    wait_for_number_of_entries_in_inbox,
)


async def test_mastodon_lone_undo_announce(blog_test_env):  # noqa F811
    undo_item = get_activity_from_json("data/mastodon_announce_1_undo.json")

    result = await blog_test_env.client.post(
        blog_test_env.local_user.get_inbox(),
        headers=fake_post_headers,
        data=json.dumps(undo_item),
    )

    assert result.status_code == 202

    await asyncio.sleep(0.3)

    await wait_for_number_of_entries_in_inbox(blog_test_env.actor, 0)
