import asyncio

from utils import get_activity_from_json
from utils.blog_test_env import (  # noqa: F401
    blog_test_env,
    wait_for_number_of_entries_in_inbox,
)


async def test_create_then_update_note(blog_test_env):  # noqa F811
    create_item = get_activity_from_json("data/mastodon_flow_1_create_note.json")
    update_item = get_activity_from_json("data/mastodon_flow_1_update_note.json")

    result = await blog_test_env.send_to_inbox(create_item)

    assert result.status_code == 202
    await wait_for_number_of_entries_in_inbox(blog_test_env, 1)

    inbox_content = await blog_test_env.get_from_inbox()
    assert len(inbox_content["orderedItems"]) == 1
    inbox_item = inbox_content["orderedItems"][0]

    assert inbox_item == "https://mastodon/users/john/statuses/9876/activity"

    result = await blog_test_env.send_to_inbox(update_item)

    await asyncio.sleep(0.3)

    # LABEL: ap-s2s-update
    await wait_for_number_of_entries_in_inbox(blog_test_env, 1)

    inbox_content = await blog_test_env.get_from_inbox()
    assert len(inbox_content["orderedItems"]) == 1
    inbox_item = inbox_content["orderedItems"][0]

    assert inbox_item["type"] == "Update"
