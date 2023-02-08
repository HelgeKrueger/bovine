from bovine_core.activitystreams.activities import build_delete
from bovine_tortoise.models import OutboxEntry

from tests.utils import get_activity_from_json
from tests.utils.blog_test_env import blog_test_env  # noqa: F401


async def test_create_then_delete(blog_test_env):  # noqa F811
    create = get_activity_from_json("data/munching_cow_create_note_1.json")
    # using a fixed delete doesn't work well with ids being assigned by the
    # server
    # delete = get_activity_from_json("data/munching_cow_delete_1.json")

    result = await blog_test_env.send_to_outbox(create)

    assert result.status_code == 202

    assert await OutboxEntry.filter(actor=blog_test_env.actor).count() == 1
    # entry = await OutboxEntry.filter(actor=blog_test_env.actor).get()
    # assert entry.content == create
    # assert (
    #     entry.local_path
    #     == "/activitypub/munchingcow/9c1d3b44-c6f6-4310-9113-a0c3d3208cac/activity"
    # )

    result = await blog_test_env.get_from_outbox()
    assert result["type"] == "OrderedCollection"
    assert result["totalItems"] == 1

    item = result["orderedItems"][0]

    delete = build_delete(blog_test_env.actor.url, item["object"]["id"]).build()

    # ap-c2s-delete-activity
    result = await blog_test_env.send_to_outbox(delete)
    assert result.status_code == 202

    assert await OutboxEntry.filter(actor=blog_test_env.actor).count() == 0

    result = await blog_test_env.get_from_outbox()
    assert result["type"] == "OrderedCollection"
    assert result["totalItems"] == 0
