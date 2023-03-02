import json
from datetime import datetime

from bovine_core.activitystreams.activities import build_create
from bovine_core.activitystreams.objects import build_note
from bovine_tortoise.models import Follower

from utils.blog_test_env import blog_test_env  # noqa: F401


import pytest


@pytest.mark.skip("FIXME should be reenabled once way to create follower is fixed")
async def test_create_note_is_send_to_user(blog_test_env):  # noqa F811
    await Follower.create(
        actor=blog_test_env.actor,
        account="other",
        followed_on=datetime.now(),
        inbox="other/inbox",
        public_key="---key---",
    )

    note = (
        build_note(blog_test_env.local_user.name, blog_test_env.local_user.url, "test")
        .as_public()
        .build()
    )

    create = build_create(note).build()

    result = await blog_test_env.send_to_outbox(create)

    assert result.status_code == 202

    result = await blog_test_env.get_from_outbox()
    assert result["id"].endswith(blog_test_env.local_user.get_outbox())  # FIXME?
    assert result["type"] == "OrderedCollection"

    assert result["totalItems"] == 1
    assert result["orderedItems"][0]["id"] != create["id"]

    blog_test_env.mock_signed_post.assert_awaited_once()

    args = blog_test_env.mock_signed_post.await_args[0]
    assert args[3] == "other/inbox"
    create_data = json.loads(args[4])

    assert create_data == result["orderedItems"][0]

    assert create_data["type"] == "Create"

    # LABEL: ap-s2s-has-object
    assert isinstance(create_data["object"], dict)
