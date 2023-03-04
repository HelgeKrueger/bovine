import uuid
from unittest.mock import AsyncMock

from .utils import update_id


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
