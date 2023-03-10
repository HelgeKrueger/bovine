import logging
import uuid

from bovine.clients.activity_pub import ActivityPubClient
from quart import current_app

from .base_count_and_items import BaseCountAndItems

logger = logging.getLogger(__name__)


class LocalActor:
    def __init__(
        self,
        name: str,
        url: str,
        public_key: str,
        private_key: str,
        actor_type: str,
        no_auth_fetch: bool = False,
    ):
        self.private_key = private_key
        self.public_key = public_key
        self.url = url
        self.name = name
        self.actor_type = actor_type
        self.no_auth_fetch = no_auth_fetch

        self.inbox_process = None
        self.outbox_process = None

        self.streams = {"inbox": BaseCountAndItems(), "outbox": BaseCountAndItems()}

        self.collection_items = None
        self.collection_item_count = None

        self.collections = {}

    def client(self):
        session = current_app.config["session"]
        return ActivityPubClient(
            session, self.get_public_key_url(), self.private_key, self.url
        )

    def set_stream(self, stream_name, obj):
        self.streams[stream_name] = obj
        return self

    def set_inbox_process(self, process):
        self.inbox_process = process
        return self

    def set_outbox_process(self, process):
        self.outbox_process = process
        return self

    def set_outbox(self, item_count, items):
        self.outbox_count_coroutine = item_count
        self.outbox_items_coroutine = items
        return self

    def get_account(self):
        return self.url

    def get_inbox(self):
        return self.url + "/inbox"

    def get_outbox(self):
        return self.url + "/outbox"

    def get_public_key_url(self):
        return self.url + "#main-key"

    def dump(self):
        logger.info(f"url: {self.url}")
        logger.info(f"name: {self.name}")
        logger.info(f"type: {self.actor_type}")

    async def process_inbox_item(self, inbox_item):
        if self.inbox_process:
            await self.inbox_process(inbox_item, self)

    async def process_outbox_item(self, activity):
        if self.outbox_process:
            await self.outbox_process(activity, self)

    def generate_uuid(self):
        return f"{self.url}/{uuid.uuid4()}"

    def add_collection(self, name, collection_id):
        if name in self.collections:
            logger.error("Overwriting collection %s for %s", name, self.url)
        self.collections[name] = collection_id
        return self
