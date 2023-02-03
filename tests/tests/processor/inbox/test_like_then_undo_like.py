import json

from bovine_tortoise.models import InboxEntry

from tests.utils import fake_post_headers, get_activity_from_json
from tests.utils.blog_test_env import (  # noqa F401
    blog_test_env,
    wait_for_number_of_entries_in_inbox,
)


async def test_mastodon_like_then_undo(blog_test_env):  # noqa F811
    like_item = get_activity_from_json("data/mastodon_like_1.json")
    undo_item = get_activity_from_json("data/mastodon_like_1_undo.json")

    like_item_id = like_item["id"]

    result = await blog_test_env.client.post(
        blog_test_env.local_user.get_inbox(),
        headers=fake_post_headers,
        data=json.dumps(like_item),
    )
    assert result.status_code == 202
    await wait_for_number_of_entries_in_inbox(blog_test_env.actor, 1)

    inbox_entry = await InboxEntry.filter(actor=blog_test_env.actor).get()

    assert inbox_entry.content_id == like_item_id

    result = await blog_test_env.client.post(
        blog_test_env.local_user.get_inbox(),
        headers=fake_post_headers,
        data=json.dumps(undo_item),
    )

    assert result.status_code == 202

    await wait_for_number_of_entries_in_inbox(blog_test_env.actor, 0)
