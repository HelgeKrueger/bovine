from bovine_core.activitystreams.activities import build_delete

from utils import get_activity_from_json
from utils.blog_test_env import blog_test_env  # noqa: F401


async def test_create_then_delete(blog_test_env):  # noqa F811
    create = get_activity_from_json("data/munching_cow_create_note_1.json")
    # using a fixed delete doesn't work well with ids being assigned by the
    # server
    # delete = get_activity_from_json("data/munching_cow_delete_1.json")

    result = await blog_test_env.send_to_outbox(create)

    assert result.status_code == 201

    result = await blog_test_env.get_from_outbox()
    assert result["type"] == "OrderedCollection"
    assert result["totalItems"] == 1

    item_id = result["orderedItems"][0]
    item = await blog_test_env.get_activity(item_id)

    delete = build_delete(blog_test_env.actor["id"], item["object"]).build()

    # ap-c2s-delete-activity
    result = await blog_test_env.send_to_outbox(delete)
    assert result.status_code == 201

    result = await blog_test_env.get_from_outbox()
    assert result["type"] == "OrderedCollection"
    assert result["totalItems"] == 2

    first_item = await blog_test_env.get_activity(result["orderedItems"][0])
    object_item = await blog_test_env.get_activity(first_item["object"])

    assert object_item["type"] == "Tombstone"
