from bovine_tortoise.models import InboxEntry

from utils import get_activity_from_json
from utils.blog_test_env import blog_test_env  # noqa F401


async def test_mastodon_delete_actor(blog_test_env):  # noqa F811
    data = get_activity_from_json("data/mastodon_delete_actor_1.json")

    result = await blog_test_env.send_to_inbox(data)

    assert result.status_code == 202
    assert await InboxEntry.filter(actor=blog_test_env.actor).count() == 0

    result_get = await blog_test_env.get_from_inbox()

    assert result_get["type"] == "OrderedCollection"
    assert result_get["totalItems"] == 0
