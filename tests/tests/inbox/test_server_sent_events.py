import asyncio

from bovine_core.types import ServerSentEvent

from bovine_core.activitystreams.activities import build_create
from bovine_core.activitystreams.objects import build_note

from tests.utils.blog_test_env import (  # noqa: F401
    blog_test_env,
    wait_for_number_of_entries_in_inbox,
)


async def send_test_with_id_to_inbox(env, test_id):
    note = (
        build_note(
            env.local_user.name,
            env.local_user.url,
            f"test {test_id}",
        )
        .as_public()
        .build()
    )
    create = build_create(note).build()

    response = await env.send_to_inbox(create)
    assert response.status_code == 202


async def test_server_sent_events(blog_test_env):  # noqa F811
    async with blog_test_env.client.request(
        blog_test_env.local_user.url + "/serverSentEvents",
        headers={
            "Accept": "text/event-stream",
            "Authorization": "Bearer test_token",
        },
    ) as connection:
        await send_test_with_id_to_inbox(blog_test_env, 1)

        data = await connection.receive()
        event = ServerSentEvent.parse(data)

        assert event.id == "1"

        await connection.disconnect()

    await send_test_with_id_to_inbox(blog_test_env, 2)

    await asyncio.sleep(0.1)

    async with blog_test_env.client.request(
        blog_test_env.local_user.url + "/serverSentEvents",
        headers={
            "Accept": "text/event-stream",
            "Authorization": "Bearer test_token",
            "Last-Event-Id": 1,
        },
    ) as connection:
        await send_test_with_id_to_inbox(blog_test_env, 3)

        data = await connection.receive()
        event = ServerSentEvent.parse(data)

        assert event.id == "2"

        data = await connection.receive()
        event = ServerSentEvent.parse(data)

        assert event.id == "3"

        await connection.disconnect()
