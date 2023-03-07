import asyncio
import os
import json
from urllib.parse import urlparse
from unittest.mock import AsyncMock, patch

import pytest

from bovine.utils.queue_manager import QueueManager
from bovine_blog import app
from bovine_tortoise import inbox_items_for_actor_from
from bovine_tortoise.utils import init
from tortoise import Tortoise

from bovine_user.config import configure_bovine_user
from bovine_store.config import configure_bovine_store
from bovine_core.types import Visibility

from . import create_actor_and_local_user, fake_post_headers, fake_get_headers

import logging

logger = logging.getLogger(__name__)


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

    def with_actor(self, actor):
        self.actor = actor
        return self

    def with_user(self, local_user):
        self.local_user = local_user
        return self

    async def send_to_inbox(self, activity):
        result = await self.client.post(
            self.actor["inbox"],
            headers=fake_post_headers,
            data=json.dumps(activity),
        )
        return result

    async def send_to_outbox(self, activity):
        # LABEL ap-c2s-post
        result = await self.client.post(
            self.actor["outbox"],
            headers=fake_post_headers,
            data=json.dumps(activity),
        )
        return result

    async def proxy(self, url):
        proxy_url = self.actor["endpoints"]["proxyUrl"]
        result = await self.client.post(
            proxy_url, headers=fake_post_headers, form={"id": url}
        )
        assert result.status_code == 200

        return await result.get_json()

    async def get(self, url, headers={}):
        parsed_url = urlparse(url)
        path = parsed_url.path
        if parsed_url.query:
            path += f"?{parsed_url.query}"
        logger.debug(f"Getting path {path} for url {url}")
        result_get = await self.client.get(
            path,
            headers=headers,
        )

        return result_get

    async def get_activity(self, url, headers={}):
        result_get = await self.get(url, headers={**fake_get_headers, **headers})

        # label fedi-objects-are-accessible-via-id-content-type
        assert result_get.status_code == 200
        assert result_get.headers["content-type"] == "application/activity+json"

        result_json = await result_get.get_json()
        assert "@context" in result_json

        return result_json

    async def get_from_inbox(self):
        return await self.get_activity(self.actor["inbox"])

    async def get_from_outbox(self):
        return await self.get_activity(self.actor["outbox"])


@pytest.fixture
async def blog_test_env() -> str:
    db_file = "test_db.sqlite3"
    db_url = f"sqlite://{db_file}"

    await init(db_url)

    app.config["validate_signature"] = AsyncMock()
    app.config["session"] = AsyncMock()

    _, local_user = await create_actor_and_local_user()
    app.config["queue_manager"] = QueueManager()
    app.config["inbox_lookup"] = inbox_items_for_actor_from

    # app.config["object_store"] = ObjectStore(db_url=db_url)

    await configure_bovine_store(app, db_url=db_url)
    await app.config["bovine_store"].init_connection()

    await configure_bovine_user(app)

    client = app.test_client()

    await app.config["bovine_user_manager"].register("alice", "alice")

    async with app.app_context():
        _, actor = await app.config["bovine_user_manager"].get_activity_pub("alice")

    actor = actor.build(visibility=Visibility.OWNER)
    public_key_url = actor["publicKey"]["id"]

    app.config["validate_signature"].return_value = public_key_url

    with patch("bovine_core.clients.signed_http.signed_post") as mock_signed_post:
        with patch("bovine_core.clients.signed_http.signed_get") as mock_signed_get:
            mock_signed_get.return_value = AsyncMock()
            mock_signed_get.return_value.raise_for_status = lambda: 1
            mock_signed_post.return_value = AsyncMock()
            mock_signed_post.return_value.raise_for_status = lambda: 1

            yield BlogTestEnv(db_url, client).with_user(local_user).with_actor(
                actor
            ).with_mocks(mock_signed_get, mock_signed_post)

    await asyncio.sleep(0.1)

    await Tortoise.close_connections()

    if not os.environ.get("KEEP_DB"):
        os.unlink(db_file)


async def wait_for_number_of_entries_in_inbox(blog_test_env, entry_number):
    for _ in range(10):
        inbox_content = await blog_test_env.get_from_inbox()

        logger.info(json.dumps(inbox_content))

        if inbox_content["totalItems"] == entry_number:
            break
        await asyncio.sleep(0.05)

    inbox_content = await blog_test_env.get_from_inbox()

    assert inbox_content["totalItems"] == entry_number
