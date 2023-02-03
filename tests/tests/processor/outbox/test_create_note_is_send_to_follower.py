import json
from datetime import datetime

from bovine_core.activitystreams.activities import build_create
from bovine_core.activitystreams.objects import build_note
from bovine_tortoise.models import Follower

from tests.utils import fake_get_headers, fake_post_headers
from tests.utils.blog_test_env import blog_test_env  # noqa: F401


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

    result = await blog_test_env.client.post(
        blog_test_env.local_user.get_outbox(),
        headers=fake_post_headers,
        data=json.dumps(create),
    )

    assert result.status_code == 202

    result = await blog_test_env.client.get(
        blog_test_env.local_user.get_outbox(),
        headers=fake_get_headers,
    )

    assert result.status_code == 200

    result_json = await result.get_json()

    assert result_json["id"].endswith(blog_test_env.local_user.get_outbox())  # FIXME?
    assert result_json["type"] == "OrderedCollection"

    assert result_json["totalItems"] == 1
    assert result_json["orderedItems"][0] == create

    blog_test_env.mock_signed_post.assert_awaited_once()

    args = blog_test_env.mock_signed_post.await_args[0]

    assert args[3] == "other/inbox"
    assert json.loads(args[4]) == create
