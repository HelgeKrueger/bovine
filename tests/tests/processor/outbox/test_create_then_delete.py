import json

from bovine_tortoise.models import OutboxEntry

from tests.utils import fake_post_headers, get_activity_from_json
from tests.utils.blog_test_env import blog_test_env  # noqa: F401


async def test_create_then_delete(blog_test_env):  # noqa F811
    create = get_activity_from_json("data/munching_cow_create_note_1.json")
    delete = get_activity_from_json("data/munching_cow_delete_1.json")

    result = await blog_test_env.client.post(
        blog_test_env.local_user.get_outbox(),
        headers=fake_post_headers,
        data=json.dumps(create),
    )

    assert result.status_code == 202

    assert await OutboxEntry.filter(actor=blog_test_env.actor).count() == 1
    entry = await OutboxEntry.filter(actor=blog_test_env.actor).get()
    assert entry.content == create
    assert entry.local_path == "munchingcow/9c1d3b44-c6f6-4310-9113-a0c3d3208cac"

    result = await blog_test_env.client.post(
        blog_test_env.local_user.get_outbox(),
        headers=fake_post_headers,
        data=json.dumps(delete),
    )

    assert result.status_code == 202

    assert await OutboxEntry.filter(actor=blog_test_env.actor).count() == 0
