import json
import logging

import aiohttp
import tomli

from bovine.clients.activity_pub import ActivityPubClient
from bovine.clients.signed_http import signed_post

from .activity_factory import ActivityFactory
from .collection_helper import CollectionHelper
from .object_factory import ObjectFactory

logger = logging.getLogger(__name__)


class ActivityPubActor:
    def __init__(self, actor_id):
        self.actor_id = actor_id
        self.client = None
        self.information = None
        self._activity_factory = None
        self._object_factory = None

    def with_http_signature(self, public_key_url, private_key, session=None):
        if session is None:
            session = aiohttp.ClientSession()

        self.client = ActivityPubClient(session, public_key_url, private_key)

        return self

    async def load(self):
        if self.client is None:
            raise Exception("Client not set in ActivityPubActor")

        response = await self.client.get(self.actor_id)
        response.raise_for_status()

        self.information = json.loads(await response.text())

        logger.debug("Retrieved information %s", self.information)

        if any(required not in self.information for required in ["inbox", "outbox"]):
            raise Exception("Retrieved incomplete actor data")

    async def send_to_outbox(self, data: dict):
        if self.information is None:
            await self.load()

        return await self.post(self.information["outbox"], data)

    async def post(self, target, data: dict):
        response = await self.client.post(target, json.dumps(data))

        response.raise_for_status()

        return response

    async def proxy_element(self, target):
        return await signed_post(
            self.client.session,
            self.client.public_key_url,
            self.client.private_key,
            self.information["endpoints"]["proxyUrl"],
            f"id={target}",
            content_type="application/x-www-form-urlencoded",
        )

    async def get_ordered_collection(self, target):
        return await self.client.get_ordered_collection(target)

    async def get(self, target):
        response = await self.client.get(target)
        response.raise_for_status()
        return json.loads(await response.text())

    async def event_source(self):
        if self.information is None:
            await self.load()

        event_source_url = self.information["endpoints"]["eventSource"]
        return self.client.event_source(event_source_url)

    @property
    def activity_factory(self):
        if self._activity_factory is None:
            self._activity_factory = ActivityFactory(self.information)
        return self._activity_factory

    @property
    def object_factory(self):
        if self._object_factory is None:
            self._object_factory = ObjectFactory(self.information)
        return self._object_factory

    @property
    def factories(self):
        return self.activity_factory, self.object_factory

    async def inbox(self):
        inbox_collection = CollectionHelper(self.information["inbox"], self)
        await inbox_collection.refresh()
        return inbox_collection

    async def outbox(self):
        inbox_collection = CollectionHelper(self.information["outbox"], self)
        await inbox_collection.refresh()
        return inbox_collection

    @staticmethod
    def from_file(filename, session):
        with open(filename, "rb") as fp:
            data = tomli.load(fp)

        actor = ActivityPubActor(data["account_url"])
        actor.with_http_signature(
            data["public_key_url"], data["private_key"], session=session
        )

        return actor
