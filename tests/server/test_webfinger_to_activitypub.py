import pytest

from bovine.test.in_memory_test_app import app
from bovine.test import remove_domain_from_url


@pytest.mark.asyncio
async def test_get_user() -> None:
    client = app.test_client()

    response = await client.get("/.well-known/webfinger?resource=acct:user")

    assert response.status_code == 200

    data = await response.get_json()

    assert data["subject"] == "acct:user@my_domain"
    assert "links" in data

    assert len(data["links"]) > 0

    self_element_list = [x for x in data["links"] if x["rel"] == "self"]

    assert len(self_element_list) == 1

    self_element = self_element_list[0]

    assert self_element["type"] == "application/activity+json"

    self_url = self_element["href"]

    response = await client.get(remove_domain_from_url(self_url))

    assert response.status_code == 200

    data = await response.get_json()

    assert isinstance(data, dict)
