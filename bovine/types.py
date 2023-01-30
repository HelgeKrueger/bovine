import json
import logging

from bovine.processors.processor_list import ProcessorList


class InboxItem:
    def __init__(self, body, authorization={}):
        self.authorization = authorization
        self.body = body
        self.data = None

    def get_data(self):
        if not self.data:
            self.data = json.loads(self.body)
        return self.data

    def get_body_id(self) -> str:
        try:
            parsed = json.loads(self.body.decode("utf-8"))
            return parsed["id"]
        except Exception as e:
            logging.info(e)
            return "failed fetching id"

    def dump(self):
        logging.info("###########################################################")
        logging.info("---AUTHORIZATION----")
        logging.info(json.dumps(self.authorization))
        logging.info("---BODY----")
        logging.info(self.body.decode("utf-8"))


class LocalUser:
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

        self.inbox_processors = ProcessorList()
        self.outbox_processors = ProcessorList()

        self.outbox_count_coroutine = None
        self.outbox_items_coroutine = None

    def add_inbox_processor(self, processor):
        self.inbox_processors.add(processor)
        return self

    def add_outbox_processor(self, processor):
        self.outbox_processors.add(processor)
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
        logging.info(f"url: {self.url}")
        logging.info(f"name: {self.name}")
        logging.info(f"type: {self.actor_type}")

    async def process_inbox_item(self, inbox_item: InboxItem):
        await self.inbox_processors.apply(inbox_item, self)

    async def process_outbox_item(self, activity, session):
        await self.outbox_processors.apply(activity, self, session)

    async def outbox_item_count(self):
        if self.outbox_count_coroutine:
            return await self.outbox_count_coroutine(self)

        return 0

    async def outbox_items(self, start=0, limit=10):
        if self.outbox_items_coroutine:
            return await self.outbox_items_coroutine(self, start, limit)

        return []
