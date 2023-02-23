import asyncio

from bovine_core.activitystreams.activities import build_create
from bovine_core.activitystreams.objects import build_note

from utils.blog_test_env import blog_test_env  # noqa: F401


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
    assert result["type"] == "OrderedCollection"
    assert result["totalItems"] == 25

    assert "first" in result
    assert "last" in result

    first_page_result = await blog_test_env.get_activity(result["first"])
    assert first_page_result["type"] == "OrderedCollectionPage"
    assert len(first_page_result["orderedItems"]) == 10

    second_page_result = await blog_test_env.get_activity(first_page_result["next"])
    assert second_page_result["type"] == "OrderedCollectionPage"
    assert len(second_page_result["orderedItems"]) == 10

    third_page_result = await blog_test_env.get_activity(second_page_result["next"])
    assert third_page_result["type"] == "OrderedCollectionPage"
    assert len(third_page_result["orderedItems"]) == 5
