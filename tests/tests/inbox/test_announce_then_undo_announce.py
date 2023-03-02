import json
from unittest.mock import AsyncMock

import pytest

from utils import get_activity_from_json
from utils.blog_test_env import (  # noqa: F401
    blog_test_env,
    wait_for_number_of_entries_in_inbox,
)


@pytest.mark.skip("FIXME: Not sure if still correct behavior")
async def test_mastodon_announce_then_undo(blog_test_env):  # noqa F811
    announce = get_activity_from_json("data/mastodon_announce_1.json")
    undo_item = get_activity_from_json("data/mastodon_announce_1_undo.json")

    # announce_id = announce["id"]

    mock_response = AsyncMock()

    blog_test_env.mock_signed_get.return_value = mock_response

    mock_response.text.return_value = json.dumps(
        get_activity_from_json("data/buffalo_create_note_1.json")
    )

    result = await blog_test_env.send_to_inbox(announce)

    await wait_for_number_of_entries_in_inbox(blog_test_env, 2)

    # FIXME: Should fetch actual object

    blog_test_env.mock_signed_get.assert_awaited()

    # FIXME: Also actor objects are fetched, account for this

    result = await blog_test_env.send_to_inbox(undo_item)

    assert result.status_code == 202

    await wait_for_number_of_entries_in_inbox(blog_test_env, 1)
