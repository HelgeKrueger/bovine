from unittest.mock import AsyncMock

import asyncio
import json

from bovine.activitystreams.activities import build_create
from bovine.activitystreams.objects import build_note

from utils.blog_test_env import (  # noqa: F401
    blog_test_env,
)


async def test_create_and_send_note(blog_test_env):  # noqa F811
    actor = blog_test_env.actor
    note = (
        build_note(actor["id"], None, "some text").add_to("http://remote_user").build()
    )
    create = build_create(note).build()

    response = AsyncMock()
    response.raise_for_status = lambda: 1
    response.text.return_value = json.dumps({"inbox": "http://remote_user/inbox"})

    blog_test_env.mock_signed_get.return_value = response
    blog_test_env.mock_signed_post.return_value = response

    result = await blog_test_env.send_to_outbox(create)

    assert result.status_code == 201

    await asyncio.sleep(0.05)

    result = await blog_test_env.get_from_outbox()
    assert result["id"] == blog_test_env.actor["outbox"]
    assert result["type"] == "OrderedCollection"
    assert result["totalItems"] == 1

    blog_test_env.mock_signed_post.assert_awaited_once()
