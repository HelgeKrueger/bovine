import re

from bovine.clients.activity_pub import ActivityPubClient

from bovine_fedi.utils.test.in_memory_test_app import app

from .local_actor import LocalActor


def test_create_object_id():
    local_actor = LocalActor("name", "url", "public_key", "private_key", "actor_type")

    new_id = local_actor.generate_uuid()

    assert re.match(
        r"url/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", new_id
    )


async def test_client():
    async with app.app_context():
        local_actor = LocalActor(
            "name", "url", "public_key", "private_key", "actor_type"
        )
        client = local_actor.client()

        assert isinstance(client, ActivityPubClient)
