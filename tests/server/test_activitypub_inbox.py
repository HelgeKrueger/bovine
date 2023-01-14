import pytest
from datetime import datetime

from bovine.test.in_memory_test_app import app


@pytest.mark.asyncio
async def test_activitypub_inbox_post_is_unauthorized_without_signature() -> None:
    client = app.test_client()

    response = await client.post("/activitypub/user/inbox")

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_activitypub_inbox_post_is_unauthorized_with_signature() -> None:
    async with app.app_context():
        client = app.test_client()

        data = "XXX"
        date = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")

        signature = (
            'keyId="other",headers="(request-target) host date digest",signature="XXX"'
        )

        response = await client.post(
            "/activitypub/user/inbox",
            headers={
                "Signature": signature,
                "date": date,
            },
            data=data,
        )

    assert response.status_code == 202
