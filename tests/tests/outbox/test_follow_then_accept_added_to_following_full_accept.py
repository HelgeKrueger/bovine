import json


import asyncio
from unittest.mock import AsyncMock

from bovine_core.activitystreams.activities import build_follow, build_accept

from utils.blog_test_env import (  # noqa: F401
    blog_test_env,
    wait_for_number_of_entries_in_inbox,
)


async def test_follow_then_accept_is_added_to_following_full_accept(
    blog_test_env,  # noqa F811
):
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

    follow = build_follow("remote", actor_id, remote_actor).build()

    # LABEL: ap-c2s-status-code

    result = await blog_test_env.send_to_outbox(follow)
    assert result.status_code == 201
    assert "location" in result.headers
    follow["id"] = result.headers["location"]

    follow_from_server = await blog_test_env.get(follow["id"])
    follow_from_server = await follow_from_server.get_json()

    assert follow_from_server["type"] == "Follow"
    assert follow_from_server["object"] == remote_actor

    await asyncio.sleep(0.3)

    accept = build_accept(remote_actor, follow).build()

    result = await blog_test_env.send_to_inbox(accept)

    assert result.status_code == 202

    await wait_for_number_of_entries_in_inbox(blog_test_env, 1)

    # LABEL: ap-s2s-accept

    following = await blog_test_env.get_activity(blog_test_env.actor["following"])

    assert following["totalItems"] == 1
    assert following["orderedItems"] == [remote_actor]
