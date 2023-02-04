from datetime import datetime

import pytest
from bovine.utils.test.in_memory_test_app import app


@pytest.mark.asyncio
async def test_activitypub_inbox_post_is_unauthorized_without_signature() -> None:
    client = app.test_client()

    response = await client.post("/activitypub/user/inbox")

    assert response.status_code == 202


@pytest.mark.asyncio
async def test_activitypub_inbox_post_is_unauthorized_with_signature() -> None:
    async with app.app_context():
        client = app.test_client()

        data = "XXX"
        date = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")

        signature = ",".join(
            [
                'keyId="other"',
                'algorithm="rsa"',
                'headers="(request-target) host date digest"',
                'signature="XXX"',
            ]
        )

        response = await client.post(
            "/activitypub/user/inbox",
            headers={
                "Signature": signature,
                "date": date,
                "host": "host",
                "digest": "XXX",
            },
            data=data,
        )

    assert response.status_code == 202
