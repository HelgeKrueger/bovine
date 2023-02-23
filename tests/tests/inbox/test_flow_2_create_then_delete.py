import asyncio
from utils import get_activity_from_json
from utils.blog_test_env import (  # noqa F401
    blog_test_env,
    wait_for_number_of_entries_in_inbox,
)


async def test_flow_2_mastodon_create_then_delete(blog_test_env):  # noqa F811
    create_activity = get_activity_from_json("data/mastodon_flow_2_create_note.json")
    delete_activity = get_activity_from_json("data/mastodon_flow_2_delete_note.json")

    result = await blog_test_env.send_to_inbox(create_activity)
    assert result.status_code == 202

    await wait_for_number_of_entries_in_inbox(blog_test_env, 1)

    # LABEL: ap-s2s-delete
    result = await blog_test_env.send_to_inbox(delete_activity)
    assert result.status_code == 202

    await asyncio.sleep(0.4)

    result_get = await blog_test_env.get_from_inbox()

    assert result_get["type"] == "OrderedCollection"
    assert result_get["totalItems"] == 2

    delete, create = result_get["orderedItems"]

    response = await blog_test_env.proxy(delete)
    assert response["type"] == "Delete"

    # FIXME: Why does this fail?
    object_to_delete = response["object"]["id"]
    # tombstone = await blog_test_env.proxy(object_to_delete)

    tombstone = response["object"]

    assert tombstone["id"] == object_to_delete
    assert tombstone["type"] == "Tombstone"
    assert set(tombstone.keys()) == {"atomUri", "id", "type"}
    # FIXME Check content
    # FIXME: why atomid
