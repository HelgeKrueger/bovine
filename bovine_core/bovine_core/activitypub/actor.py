import json

import aiohttp
import tomli

from bovine_core.activitystreams.objects import build_note
from bovine_core.clients.activity_pub import ActivityPubClient


class ActivityPubActor:
    def __init__(self, actor_id):
        self.actor_id = actor_id
        self.client = None
        self.information = None

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

        if any(required not in self.information for required in ["inbox", "outbox"]):
            raise Exception("Retrieved incomplete actor data")

    async def send_to_outbox(self, data: dict):
        if self.information is None:
            await self.load()

        response = await self.client.post(self.information["outbox"], json.dumps(data))

        response.raise_for_status()

        return response

    async def get(self, target):
        response = await self.client.get(target)
        response.raise_for_status()
        return json.loads(await response.text())

    async def event_source(self):
        if self.information is None:
            await self.load()

        event_source_url = self.information["endpoints"]["eventSource"]
        return self.client.event_source(event_source_url)

    def note(self, text):
        return build_note(self.actor_id, "", text)

    @staticmethod
    def from_file(filename, session):
        with open(filename, "rb") as fp:
            data = tomli.load(fp)

        actor = ActivityPubActor(data["account_url"])
        actor.with_http_signature(
            data["public_key_url"], data["private_key"], session=session
        )

        return actor
