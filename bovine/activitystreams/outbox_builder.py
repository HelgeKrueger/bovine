class OutboxBuilder:
    def __init__(self, url):
        self.url = url
        self.items = []
        self.count = 0

    def with_items(self, items):
        self.items = items
        return self

    def with_count(self, count):
        self.count = count
        return self

    def build(self):
        return {
            "@context": "https://www.w3.org/ns/activitystreams",
            "id": self.url,
            "orderedItems": self.items,
            "totalItems": self.count,
            "type": "OrderedCollection",
        }
