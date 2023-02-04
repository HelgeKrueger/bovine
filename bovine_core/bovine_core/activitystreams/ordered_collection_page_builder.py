from .common import build_context


class OrderedCollectionPageBuilder:
    def __init__(self, url: str, part_of: str):
        self.context_builder = build_context()
        self.url = url
        self.items: list = []
        self.part_of = part_of
        self.next: str | None = None
        self.prev: str | None = None

    def with_items(self, items: list):
        self.items = items
        return self

    def with_next(self, url):
        self.next = url
        return self

    def with_prev(self, url):
        self.prev = url
        return self

    def build(self) -> dict:
        result = {
            "@context": self.context_builder.build(),
            "id": self.url,
            "partOf": self.part_of,
            "orderedItems": self.items,
            "type": "OrderedCollectionPage",
        }

        if self.next:
            result["next"] = self.next

        if self.prev:
            result["prev"] = self.prev

        return result
