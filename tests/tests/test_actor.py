from tests.utils.blog_test_env import blog_test_env  # noqa: F401


async def test_actor(blog_test_env):  # noqa: F811
    result = await blog_test_env.get_activity("/activitypub/name")

    assert result["type"] == "Person"
    assert "inbox" in result
    assert "outbox" in result

    # LABEL: ap-actor-preferredUsername
    assert isinstance(result["preferredUsername"], str)

    inbox_result = await blog_test_env.get_activity(result["inbox"])
    # LABEL: ap-actor-inbox
    assert inbox_result["type"] == "OrderedCollection"

    outbox_result = await blog_test_env.get_activity(result["outbox"])
    # LABEL: ap-actor-outbox
    assert outbox_result["type"] == "OrderedCollection"
