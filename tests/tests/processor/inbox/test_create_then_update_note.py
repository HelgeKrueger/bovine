from tests.utils import get_activity_from_json
from tests.utils.blog_test_env import (  # noqa: F401
    blog_test_env,
    wait_for_number_of_entries_in_inbox,
)


async def test_create_then_update_note(blog_test_env):  # noqa F811
    create_item = get_activity_from_json("data/mastodon_flow_1_create_note.json")
    update_item = get_activity_from_json("data/mastodon_flow_1_update_note.json")

    result = await blog_test_env.send_to_inbox(create_item)

    assert result.status_code == 202
    await wait_for_number_of_entries_in_inbox(blog_test_env.actor, 1)

    result = await blog_test_env.send_to_inbox(update_item)

    # FIXME: There should only be one item in inbox
    # FIXME: Content of item should be updated
    await wait_for_number_of_entries_in_inbox(blog_test_env.actor, 2)
