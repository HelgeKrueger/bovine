import json
from unittest.mock import AsyncMock

from tests.utils import fake_post_headers, get_activity_from_json
from tests.utils.blog_test_env import (  # noqa: F401
    blog_test_env,
    wait_for_number_of_entries_in_inbox,
)


async def test_mastodon_announce_then_undo(blog_test_env):  # noqa F811
    announce = get_activity_from_json("data/mastodon_announce_1.json")
    undo_item = get_activity_from_json("data/mastodon_announce_1_undo.json")

    # announce_id = announce["id"]

    mock_response = AsyncMock()

    blog_test_env.mock_signed_get.return_value = mock_response

    mock_response.text.return_value = json.dumps(
        get_activity_from_json("data/buffalo_create_note_1.json")
    )

    result = await blog_test_env.client.post(
        blog_test_env.local_user.get_inbox(),
        headers=fake_post_headers,
        data=json.dumps(announce),
    )

    await wait_for_number_of_entries_in_inbox(blog_test_env.actor, 2)

    # inbox_entry = await InboxEntry.filter(actor=blog_test_env.actor).get()

    # assert inbox_entry.content_id == announce_id
    # assert inbox_entry.content["type"] == "Announce"

    # FIXME: Should fetch actual object

    blog_test_env.mock_signed_get.assert_awaited_once()

    result = await blog_test_env.client.post(
        blog_test_env.local_user.get_inbox(),
        headers=fake_post_headers,
        data=json.dumps(undo_item),
    )

    assert result.status_code == 202

    await wait_for_number_of_entries_in_inbox(blog_test_env.actor, 1)
