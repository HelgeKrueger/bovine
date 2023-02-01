from unittest.mock import AsyncMock

import pytest
from quart import g, request

from bovine_core.utils.date import get_gmt_now
from bovine.utils.test.in_memory_test_app import app

from .rewrite_request import rewrite_activity_request


async def test_basic_get_accept_header():
    async with app.test_request_context("/", method="GET"):
        await rewrite_activity_request()

        assert request.path == "/"

    async with app.test_request_context(
        "/", method="GET", headers={"accept": "application/activity+json"}
    ):
        await rewrite_activity_request()

        assert request.path == "/activitypub/"
        assert g.signature_result is None


async def test_basic_get_accept_header_and_signature():
    app.config["validate_signature"] = AsyncMock()
    app.config["validate_signature"].return_value = "valid_key"

    async with app.test_request_context(
        "/",
        method="GET",
        headers={
            "accept": "application/activity+json",
            "signature": "fake_signature",
            "date": get_gmt_now(),
        },
    ):
        await rewrite_activity_request()

        assert request.path == "/activitypub/"
        assert g.signature_result == "valid_key"
        assert g.authorized_user is None

        app.config["validate_signature"].assert_awaited_once()


@pytest.mark.skip("not the behavior anymore, support for form encoded data")
async def test_basic_post_accept_header():
    async with app.test_request_context("/", method="POST"):
        await rewrite_activity_request()

        assert request.path == "/"

    async with app.test_request_context(
        "/", method="POST", headers={"content-type": "application/activity+json"}
    ):
        await rewrite_activity_request()

        assert request.path == "/activitypub/"

    async with app.test_request_context(
        "/activitypub",
        method="POST",
        headers={"content-type": "application/activity+json"},
    ):
        await rewrite_activity_request()

        assert request.path == "/activitypub"


async def test_basic_get_authorization():
    app.config["validate_signature"] = AsyncMock()
    app.config["validate_signature"].return_value = None

    app.config["account_name_or_none_for_token"] = AsyncMock()
    app.config["account_name_or_none_for_token"].return_value = "my_account"

    async with app.test_request_context(
        "/",
        method="GET",
        headers={
            "accept": "application/activity+json",
            "authorization": "Bearer my_token_cow",
            "date": get_gmt_now(),
        },
    ):
        await rewrite_activity_request()

        assert request.path == "/activitypub/"
        assert g.signature_result is None
        assert g.authorized_user == "my_account"

        app.config["account_name_or_none_for_token"].assert_awaited_once_with(
            "my_token_cow"
        )
