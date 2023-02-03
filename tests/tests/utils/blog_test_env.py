import asyncio
import os
from unittest.mock import AsyncMock, patch

import pytest
from bovine_blog import app
from bovine_tortoise import init
from bovine_tortoise.models import InboxEntry
from tortoise import Tortoise

from . import create_actor_and_local_user


class BlogTestEnv:
    def __init__(self, db_url, client):
        self.db_url = db_url
        self.actor = None
        self.local_user = None
        self.client = client
        self.mock_signed_get = None
        self.mock_signed_post = None

    def with_mocks(self, mock_signed_get, mock_signed_post):
        self.mock_signed_get = mock_signed_get
        self.mock_signed_post = mock_signed_post
        return self

    def with_user(self, actor, local_user):
        self.actor = actor
        self.local_user = local_user
        return self


@pytest.fixture
async def blog_test_env() -> str:
    db_file = "test_db.sqlite3"
    db_url = f"sqlite://{db_file}"

    await init(db_url)

    app.config["validate_signature"] = AsyncMock()
    app.config["session"] = AsyncMock()

    actor, local_user = await create_actor_and_local_user()
    app.config["validate_signature"].return_value = local_user.get_public_key_url()

    client = app.test_client()

    with patch("bovine_core.clients.signed_http.signed_post") as mock_signed_post:
        with patch("bovine_core.clients.signed_http.signed_get") as mock_signed_get:
            yield BlogTestEnv(db_url, client).with_user(actor, local_user).with_mocks(
                mock_signed_get, mock_signed_post
            )

    await Tortoise.close_connections()

    os.unlink(db_file)


async def wait_for_number_of_entries_in_inbox(actor, entry_number):
    while await InboxEntry.filter(actor=actor).count() != entry_number:
        await asyncio.sleep(0.01)

    assert await InboxEntry.filter(actor=actor).count() == entry_number
