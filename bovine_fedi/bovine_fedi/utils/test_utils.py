import uuid
from unittest.mock import AsyncMock

from . import determine_local_path_from_activity_id, update_id


async def test_update_id():
    async def id_generator():
        return str(uuid.uuid4())

    store = AsyncMock()
    store.id_generator = id_generator

    data = {"id": "id"}
    result = await update_id(data, "retriever", store)
    assert result["id"] != "id"

    data = {"object": "test"}
    result = await update_id(data, "retriever", store)
    assert result["id"]

    # if in store; id is not updated
    data = {"object": {"id": "id"}}
    result = await update_id(data, "retriever", store)
    assert result["object"]["id"] == "id"

    store.retrieve.return_value = None
    data = {"object": {"id": "id"}}
    result = await update_id(data, "retriever", store)
    assert result["object"]["id"] != "id"


def test_determine_local_path():
    activity_id = "https://domain/something/name/uuid/delete"

    local_path = determine_local_path_from_activity_id(activity_id)

    assert local_path == "/something/name/uuid/delete"
