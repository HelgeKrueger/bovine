import json
from unittest.mock import AsyncMock, patch

from bovine.types import LocalActor, ProcessingItem
from bovine.utils.test.in_memory_test_app import app
from bovine_store.utils.test import store  # noqa F401

from .incoming_actor import incoming_actor


async def test_incoming_actor_failure_to_retrieve(store):  # noqa F801
    async with app.app_context():
        first_id = "https://my_domain/first"
        actor_url = "https://my_domain/actor"
        item = {
            "@context": "https://www.w3.org/ns/activitystreams",
            "actor": actor_url,
            "id": first_id,
            "type": "Like",
        }

        local_actor = LocalActor(
            "name", "local_actor_url", "public_key", "private_key", "actor_type"
        )

        processing_item = ProcessingItem(json.dumps(item))

        result = await incoming_actor(processing_item, local_actor)

        assert result == processing_item
        assert result.get_data()["actor"] == actor_url


@patch("bovine_core.clients.signed_http.signed_get")
async def test_incoming_actor_succes(mock_signed_get, store):  # noqa F801
    async with app.app_context():
        first_id = "https://my_domain/first"
        actor_url = "https://my_domain/actor"
        item = {
            "@context": "https://www.w3.org/ns/activitystreams",
            "actor": actor_url,
            "id": first_id,
            "type": "Like",
        }
        actor_object = {
            "@context": "https://www.w3.org/ns/activitystreams",
            "id": actor_url,
            "name": "remote actor",
        }
        mock_signed_get.return_value = AsyncMock()
        mock_signed_get.return_value.text.return_value = json.dumps(actor_object)

        local_actor = LocalActor(
            "name", "local_actor_url", "public_key", "private_key", "actor_type"
        )

        processing_item = ProcessingItem(json.dumps(item))

        result = await incoming_actor(processing_item, local_actor)

        assert result == processing_item
        item_actor = result.get_data()["actor"]
        assert set(item_actor.keys()) == {"id", "name"}
        assert item_actor["name"] == "remote actor"
