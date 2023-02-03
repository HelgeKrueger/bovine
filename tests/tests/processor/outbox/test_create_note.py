import json

from bovine_tortoise.models import OutboxEntry

from tests.utils import fake_get_headers, fake_post_headers, get_activity_from_json
from tests.utils.blog_test_env import blog_test_env  # noqa: F401


async def test_buffalo_create_note(blog_test_env):  # noqa F811
    item = get_activity_from_json("data/buffalo_create_note_1.json")

    result = await blog_test_env.client.post(
        blog_test_env.local_user.get_outbox(),
        headers=fake_post_headers,
        data=json.dumps(item),
    )

    assert result.status_code == 202

    assert await OutboxEntry.filter(actor=blog_test_env.actor).count() == 1
    entry = await OutboxEntry.filter(actor=blog_test_env.actor).get()
    assert entry.content == item

    result = await blog_test_env.client.get(
        blog_test_env.local_user.get_outbox(),
        headers=fake_get_headers,
    )

    assert result.status_code == 200

    result_json = await result.get_json()

    assert result_json["id"].endswith(blog_test_env.local_user.get_outbox())  # FIXME?
    assert result_json["type"] == "OrderedCollection"

    assert result_json["totalItems"] == 1
    assert result_json["orderedItems"][0] == item
