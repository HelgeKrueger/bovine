import json

from bovine.utils.test.in_memory_test_app import (  # noqa F401
    test_client_with_bearer_authorization,
    test_client_without_authorization,
)


async def test_activitypub_post_to_outbox(
    test_client_without_authorization,  # noqa F811
) -> None:
    response = await test_client_without_authorization.post(
        "/activitypub/user/outbox",
        data=json.dumps({"test": "xxx"}),
        headers={"Accept": "application/activity+json"},
    )

    data = await response.get_json()

    assert response.status_code == 401
    assert data == {"status": "access denied"}


async def test_activitypub_post_with_token(
    test_client_with_bearer_authorization,  # noqa F811
) -> None:
    response = await test_client_with_bearer_authorization.post(
        "/activitypub/user/outbox",
        data=json.dumps({"test": "xxx"}),
        headers={
            "Accept": "application/activity+json",
            "Content-Type": "application/activity+json",
            "Authorization": "Bearer test_token",
        },
    )

    data = await response.get_json()

    assert data == {"status": "success"}
