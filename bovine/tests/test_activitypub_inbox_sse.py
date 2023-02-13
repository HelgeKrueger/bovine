from datetime import datetime
import json

from bovine.utils.test.in_memory_test_app import (  # noqa F401
    test_client_with_authorization,
)


async def test_activitypub_server_side_events(
    test_client_with_authorization,  # noqa F811
) -> None:
    date = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
    signature = ",".join(
        [
            'keyId="other"',
            'algorithm="rsa"',
            'headers="(request-target) host date digest"',
            'signature="XXX"',
        ]
    )

    async with test_client_with_authorization.request(
        "/activitypub/user/serverSideEvents",
        headers={
            "Accept": "text/event-stream",
            "Authorization": "Bearer test_token",
        },
    ) as connection:
        response = await test_client_with_authorization.post(
            "/activitypub/user/inbox",
            data=json.dumps({"test": "xxx"}),
            headers={
                "Accept": "application/activity+json",
                "Content-Type": "application/activity+json",
                "Signature": signature,
                "date": date,
                "host": "host",
                "digest": "XXX",
            },
        )
        assert response.status_code == 202

        data = await connection.receive()
        data = data.decode("utf-8")

        assert data == 'data: {"test": "xxx"}\nevent: outbox\n\n'

        await connection.disconnect()
