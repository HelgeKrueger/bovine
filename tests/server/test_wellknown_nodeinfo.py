import json

import jsonschema
import pytest

from bovine.utils.test.in_memory_test_app import app


def validate_nodeinfo(data):
    with open("schemas/nodeinfo_2_0.schema.json", "r", encoding="utf-8") as schema_file:
        schema = json.load(schema_file)

    jsonschema.validate(data, schema)


@pytest.mark.asyncio
async def test_nodeinfo() -> None:
    client = app.test_client()

    response = await client.get("/.well-known/nodeinfo")
    data = await response.get_json()

    assert "links" in data
    assert data["links"][0]["rel"] == "http://nodeinfo.diaspora.software/ns/schema/2.0"

    nodeinfo_url = data["links"][0]["href"]
    assert nodeinfo_url == "https://my_domain/info/nodeinfo2_0"

    response = await client.get(nodeinfo_url)
    data = await response.get_json()

    assert isinstance(data, dict)

    validate_nodeinfo(data)
