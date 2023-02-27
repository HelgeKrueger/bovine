from utils.blog_test_env import blog_test_env  # noqa: F401


async def test_webfinger(blog_test_env):  # noqa: F811
    username = "name"
    account_name = f"{username}@my_domain"

    result = await blog_test_env.get(
        f"/.well-known/webfinger?resource=acct:{account_name}"
    )
    assert result.status_code == 200

    # LABEL: webfinger-content-type
    assert result.headers["content-type"] == "application/jrd+json"

    result_data = await result.get_json()

    # LABEL: webfinger-subject
    assert result_data["subject"] == f"acct:{account_name}"

    # LABEL: fedi-webfinger-self
    links = result_data["links"]
    self_element = None
    for link in links:
        if link["rel"] == "self":
            assert self_element is None
            self_element = link

    assert self_element["type"] == "application/activity+json"

    # LABEL: fedi-webfinger-username-is-preferredUsername
    actor_result = await blog_test_env.get_activity(self_element["href"])
    assert actor_result["preferredUsername"] == username


async def test_webfinger_alice(blog_test_env):  # noqa: F811
    username = "alice"
    account_name = f"{username}@my_domain"

    result = await blog_test_env.get(
        f"/.well-known/webfinger?resource=acct:{account_name}"
    )
    assert result.status_code == 200

    # LABEL: webfinger-content-type
    assert result.headers["content-type"] == "application/jrd+json"

    result_data = await result.get_json()

    # LABEL: webfinger-subject
    assert result_data["subject"] == f"acct:{account_name}"

    # LABEL: fedi-webfinger-self
    links = result_data["links"]
    self_element = None
    for link in links:
        if link["rel"] == "self":
            assert self_element is None
            self_element = link

    assert self_element["type"] == "application/activity+json"

    # LABEL: fedi-webfinger-username-is-preferredUsername
    actor_result = await blog_test_env.get_activity(self_element["href"])
    assert actor_result["preferredUsername"] == username
