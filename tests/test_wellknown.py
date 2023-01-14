import pytest

from app import app


@pytest.mark.asyncio
async def test_base() -> None:
    client = app.test_client()

    response = await client.get("/.well-known/nodeinfo")
    data = await response.get_json()

    assert "links" in data
    assert data["links"][0]["rel"] == "http://nodeinfo.diaspora.software/ns/schema/2.0"
