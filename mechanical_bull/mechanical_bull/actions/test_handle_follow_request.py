from unittest.mock import AsyncMock

from bovine_core.activitystreams.activities import build_follow

from .handle_follow_request import handle_follow_request


async def test_does_nothing_on_random_activity():
    data = {"type": "Note"}

    client = AsyncMock()

    await handle_follow_request(client, data)

    client.send_to_outbox.assert_not_awaited()


async def test_replies_to_follow_with_accept():
    data = build_follow("domain", "actor", "tofollow").build()
    client = AsyncMock()

    await handle_follow_request(client, data)

    client.send_to_outbox.assert_awaited_once()
