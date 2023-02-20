import uuid

from quart import g

from .app_env import app


async def test_retrieve():
    client = app.test_client()

    async with app.app_context():
        g.actor_url = "test"

        response = await client.get("/" + str(uuid.uuid4()))

        assert response.status_code == 200
