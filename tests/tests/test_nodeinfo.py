from utils.blog_test_env import blog_test_env  # noqa: F401


async def test_nodeinfo(blog_test_env):  # noqa: F811
    result = await blog_test_env.get("/.well-known/nodeinfo")
    data = await result.get_json()
    url = data["links"][0]["href"]

    result = await blog_test_env.get(url)
    data = await result.get_json()

    user_count = data["usage"]["users"]["total"]

    assert user_count == 1
