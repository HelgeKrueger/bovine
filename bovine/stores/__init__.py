from bovine.processors import InboxItem


class LocalUser:
    def __init__(self, name, url, public_key, private_key, actor_type):
        self.private_key = private_key
        self.public_key = public_key
        self.url = url
        self.name = name
        self.actor_type = actor_type

        self.processors = []

    def add_inbox_processor(self, processor):
        self.processors.append(processor)
        return self

    def get_inbox(self):
        return self.url + "/inbox"

    def get_outbox(self):
        return self.url + "/outbox"

    def get_public_key_url(self):
        return self.url + "#main-key"

    def dump(self):
        print(f"url: {self.url}")
        print(f"name: {self.name}")
        print(f"type: {self.actor_type}")

    async def process_inbox_item(self, inbox_item: InboxItem):
        working = inbox_item
        try:
            for processor in self.processors:
                working = await processor(self, working)
                if not working:
                    return
        except Exception as e:
            print(">>>>> SOMETHING WENT WRONG IN INBOX PROCESSING <<<<<<")
            print()
            print(e)
            print()
            inbox_item.dump()

    async def outbox_item_count(self):
        return 0

    async def outbox_items(self, start=0, limit=10):
        return []
