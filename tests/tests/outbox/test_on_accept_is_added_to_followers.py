import json

from bovine.activitystreams.activities import build_create
from bovine.activitystreams.objects import build_note


import asyncio
from unittest.mock import AsyncMock

from bovine.activitystreams.activities import build_follow, build_accept

from utils.blog_test_env import (  # noqa: F401
    blog_test_env,
    wait_for_number_of_entries_in_inbox,
)


async def test_on_accept_is_added_to_followers(blog_test_env):  # noqa F811
    remote_actor = "https://remote/actor"

    mock_response = AsyncMock()
    blog_test_env.mock_signed_get.return_value = mock_response
    mock_response.text.return_value = json.dumps(
        {
            "@context": "https://www.w3.org/ns/activitystreams",
            "id": remote_actor,
            "type": "Person",
            "inbox": f"{remote_actor}/inbox",
        }
    )
    mock_response.raise_for_status = lambda: 1

    actor_id = blog_test_env.actor["id"]

    follow = build_follow("remote", remote_actor, actor_id).build()

    result = await blog_test_env.send_to_inbox(follow)
    assert result.status_code == 202

    await wait_for_number_of_entries_in_inbox(blog_test_env, 1)

    # LABEL: ap-s2s-follow

    accept = build_accept(actor_id, follow).build()

    result = await blog_test_env.send_to_outbox(accept)
    assert result.status_code == 201

    assert "location" in result.headers
    new_location = result.headers["location"]

    accept_from_server = await blog_test_env.get(new_location)
    accept_from_server = await accept_from_server.get_json()

    assert accept_from_server["object"] == follow["id"]

    accept_from_server = await blog_test_env.proxy(new_location)

    await asyncio.sleep(0.3)

    # LABLE: ap-s2s-follow-accept
    # LABEL: ap-c2s-follow-activity

    followers = await blog_test_env.get_activity(blog_test_env.actor["followers"])

    assert followers["totalItems"] == 1
    assert followers["orderedItems"] == [remote_actor]

    note = (
        build_note(blog_test_env.actor["name"], blog_test_env.actor["id"], "test")
        .as_public(followers=blog_test_env.actor["followers"])
        .build()
    )

    create = build_create(note).build()

    result = await blog_test_env.send_to_outbox(create)

    assert result.status_code == 201

    result = await blog_test_env.get_from_outbox()
    assert result["id"] == blog_test_env.actor["outbox"]
    assert result["type"] == "OrderedCollection"

    assert result["totalItems"] == 2
    assert result["orderedItems"][0] != create["id"]

    args = blog_test_env.mock_signed_post.await_args[0]
    assert args[3] == f"{remote_actor}/inbox"
    create_data = json.loads(args[4])

    assert create_data["id"] == result["orderedItems"][0]

    assert create_data["type"] == "Create"

    # LABEL: ap-s2s-has-object
    assert isinstance(create_data["object"], dict)
