import pytest
import uuid

from quart import g

from .app_env import app


@pytest.mark.skip("FIXME")
async def test_retrieve():
    client = app.test_client()

    async with app.app_context():
        g.signature_result = "test"

        response = await client.get("/" + str(uuid.uuid4()))

        assert response.status_code == 200
