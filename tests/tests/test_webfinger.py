import xml.etree.ElementTree as ET

from utils.blog_test_env import blog_test_env  # noqa: F401


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


async def test_webfinger_unknown(blog_test_env):  # noqa: F811
    username = "unknown"
    account_name = f"{username}@my_domain"

    result = await blog_test_env.get(
        f"/.well-known/webfinger?resource=acct:{account_name}"
    )
    assert result.status_code == 404


async def test_webfinger_host_meta(blog_test_env):  # noqa: F811
    result = await blog_test_env.get("/.well-known/host-meta")

    assert result.status_code == 200

    raw_xml = await result.get_data()
    parsed = ET.fromstring(raw_xml)

    link_element = parsed.find("{http://docs.oasis-open.org/ns/xri/xrd-1.0}Link")
    assert link_element is not None

    template = link_element.get("template")

    account_uri = "acct:alice@my_domain"

    url = template.replace("{uri}", account_uri)

    result = await blog_test_env.get(url)

    assert result.status_code == 200
