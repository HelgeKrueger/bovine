from utils.blog_test_env import blog_test_env  # noqa: F401


async def test_actor(blog_test_env):  # noqa: F811
    result = await blog_test_env.get_activity(blog_test_env.actor["id"])

    assert result["type"] == "Person"
    assert "inbox" in result
    assert "outbox" in result
    assert "endpoints" in result

    # LABEL: ap-actor-preferredUsername
    assert isinstance(result["preferredUsername"], str)

    inbox_result = await blog_test_env.get_activity(result["inbox"])
    # LABEL: ap-actor-inbox
    assert inbox_result["type"] == "OrderedCollection"

    outbox_result = await blog_test_env.get_activity(result["outbox"])
    # LABEL: ap-actor-outbox
    assert outbox_result["type"] == "OrderedCollection"

    # LABEL: ap-actor-following
    following_result = await blog_test_env.get_activity(result["following"])
    # LABEL: ap-collections-following
    assert following_result["type"] == "OrderedCollection"

    # LABEL: ap-actor-followers
    followers_result = await blog_test_env.get_activity(result["followers"])
    # LABEL: ap-collections-followers
    assert followers_result["type"] == "OrderedCollection"

    # LABEL: ap-actor-endpoints
    assert "endpoints" in result

    # LABEL: ap-actor-endpoints-proxyUrl
    assert "proxyUrl" in result["endpoints"]
