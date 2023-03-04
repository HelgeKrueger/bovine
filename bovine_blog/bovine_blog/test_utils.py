import uuid

from .utils import update_id


async def test_update_id():
    async def id_generator():
        return str(uuid.uuid4())

    data = {"id": "id"}
    result = await update_id(data, id_generator)
    assert result["id"] != "id"

    data = {"object": "test"}
    result = await update_id(data, id_generator)
    assert result["id"]

    data = {"object": {"id": "id"}}
    result = await update_id(data, id_generator)
    assert result["object"]["id"] != "id"
