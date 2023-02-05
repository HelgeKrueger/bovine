import asyncio

from bovine_core.activitystreams.activities import build_create
from bovine_core.activitystreams.objects import build_note

from tests.utils.blog_test_env import blog_test_env  # noqa: F401


async def test_create_many_notes(blog_test_env):  # noqa F811
    for j in range(25):
        note = (
            build_note(
                blog_test_env.local_user.name, blog_test_env.local_user.url, f"test {j}"
            )
            .as_public()
            .build()
        )
        create = build_create(note).build()

        result = await blog_test_env.send_to_outbox(create)
        assert result.status_code == 202
        await asyncio.sleep(0.01)

    result = await blog_test_env.get_from_outbox()
    assert result.status_code == 200

    result_json = await result.get_json()
    assert result_json["type"] == "OrderedCollection"

    assert result_json["totalItems"] == 25

    assert "first" in result_json
    assert "last" in result_json

    first_page_result = await blog_test_env.get_activity(result_json["first"])
    assert first_page_result.status_code == 200

    print(result_json)

    first_page_result = await first_page_result.get_json()
    assert first_page_result["type"] == "OrderedCollectionPage"

    assert len(first_page_result["orderedItems"]) == 10

    second_page_result = await blog_test_env.get_activity(first_page_result["next"])
    assert second_page_result.status_code == 200

    second_page_result = await second_page_result.get_json()
    assert second_page_result["type"] == "OrderedCollectionPage"

    assert len(second_page_result["orderedItems"]) == 10

    third_page_result = await blog_test_env.get_activity(second_page_result["next"])
    assert third_page_result.status_code == 200

    third_page_result = await third_page_result.get_json()
    assert third_page_result["type"] == "OrderedCollectionPage"

    assert len(third_page_result["orderedItems"]) == 5
