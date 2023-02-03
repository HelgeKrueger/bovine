import json

from bovine_tortoise.models import InboxEntry

from tests.utils import fake_get_headers, fake_post_headers, get_activity_from_json
from tests.utils.blog_test_env import blog_test_env  # noqa F401


async def test_mastodon_delete_actor(blog_test_env):  # noqa F811
    data = get_activity_from_json("data/mastodon_delete_actor_1.json")

    result = await blog_test_env.client.post(
        blog_test_env.local_user.get_inbox(),
        headers=fake_post_headers,
        data=json.dumps(data),
    )

    assert result.status_code == 202
    assert await InboxEntry.filter(actor=blog_test_env.actor).count() == 0

    result_get = await blog_test_env.client.get(
        blog_test_env.local_user.get_inbox(),
        headers=fake_get_headers,
    )

    assert result_get.status_code == 200

    data = await result_get.get_json()

    # FIXME This has the wrong format; should be an ordered collection
    assert len(data) == 0
