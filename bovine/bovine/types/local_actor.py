import uuid
import logging

from .base_count_and_items import BaseCountAndItems
from .processing_item import ProcessingItem

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

    async def process_inbox_item(self, inbox_item: ProcessingItem, session):
        if self.inbox_process:
            await self.inbox_process(inbox_item, self, session)

    async def process_outbox_item(self, activity: ProcessingItem, session):
        if self.outbox_process:
            await self.outbox_process(activity, self, session)

    def item_count_for(self, stream_name: str):
        async def item_count():
            return await self.streams[stream_name].item_count(self)

        return item_count

    def items_for(self, stream_name: str):
        async def items(**kwargs):
            return await self.streams[stream_name].items(self, **kwargs)

        return items

    def generate_uuid(self):
        return f"{self.url}/{uuid.uuid4()}"
