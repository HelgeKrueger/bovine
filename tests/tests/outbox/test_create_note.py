import asyncio

from utils import get_activity_from_json
from utils.blog_test_env import (  # noqa: F401
    blog_test_env,
)


async def test_buffalo_create_note(blog_test_env):  # noqa F811
    item = get_activity_from_json("data/buffalo_create_note_1.json")

    result = await blog_test_env.send_to_outbox(item)

    assert result.status_code == 201

    await asyncio.sleep(0.05)

    result = await blog_test_env.get_from_outbox()
    assert result["id"] == blog_test_env.actor["outbox"]
    assert result["type"] == "OrderedCollection"

    # LABEL: ap-c2s-add-to-outbox
    assert result["totalItems"] == 1
    created_item_id = result["orderedItems"][0]

    created_item = await blog_test_env.get_activity(created_item_id)

    assert item["id"] != created_item["id"]

    assert created_item["type"] == "Create"
    if isinstance(created_item["object"], str):
        object_item = await blog_test_env.get_activity(created_item["object"])
    else:
        object_item = created_item["object"]

    assert object_item["type"] == "Note"
    # LABEL: ap-c2s-new-id
    assert object_item["id"] != item["object"]["id"]

    # LABEL: fedi-objects-are-accessible-via-id
    object_id = object_item["id"]

    result = await blog_test_env.get_activity(object_id)
    assert result["type"] == "Note"
    assert "@context" in result

    #
    # FIXME: Decide what behavior I want here
    #

    # LABEL: fedi-objects-have-html-representations
    # redirect = await blog_test_env.get(object_id, headers={"Accept": "text/html"})
    # assert redirect.status_code == 302

    # new_location = redirect.headers["location"]
    # html_representation = await blog_test_env.get(
    #     new_location, headers={"Accept": "text/html"}
    # )

    # assert html_representation.status_code == 200
    # html_content = await html_representation.get_data(as_text=True)

    # assert "literally creating test data" in html_content
