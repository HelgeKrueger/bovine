import asyncio
import json

from bovine_tortoise.models import Follower

from tests.utils import fake_post_headers, get_activity_from_json
from tests.utils.blog_test_env import blog_test_env  # noqa: F401


async def test_mastodon_follow_request_is_accepted(blog_test_env):  # noqa: F811
    item = get_activity_from_json("data/mastodon_follow_1.json")

    result = await blog_test_env.client.post(
        blog_test_env.local_user.get_inbox(),
        headers=fake_post_headers,
        data=json.dumps(item),
    )

    assert result.status_code == 202

    while blog_test_env.mock_signed_post.await_count == 0:
        await asyncio.sleep(0.1)

    blog_test_env.mock_signed_post.assert_awaited_once()

    args = blog_test_env.mock_signed_post.await_args[0]
    assert args[1] == blog_test_env.local_user.get_public_key_url()
    assert args[2] == "private_key"
    # assert args[3] == "inbox"
    # FIXME the logic for generating the inbox name is broken

    response_activity = json.loads(args[4])
    assert response_activity["type"] == "Accept"
    assert response_activity["object"] == item

    assert await Follower.filter(actor=blog_test_env.actor).count() == 1

    entry = await Follower.filter(actor=blog_test_env.actor).get()
    assert entry.account == "https://example.com/users/JohnMastodon"
