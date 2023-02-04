from .common import build_context


class OrderedCollectionBuilder:
    def __init__(self, url: str):
        self.context_builder = build_context()
        self.url = url
        self.items: list | None = None
        self.count = 0
        self.first = None
        self.last = None

    def with_items(self, items: list):
        self.items = items
        return self

    def with_count(self, count: int):
        self.count = count
        return self

    def with_first_and_last(self, first, last):
        self.first = first
        self.last = last
        return self

    def build(self) -> dict:
        result = {
            "@context": self.context_builder.build(),
            "id": self.url,
            "totalItems": self.count,
            "type": "OrderedCollection",
        }

        if self.items:
            result["orderedItems"] = self.items

        if self.first:
            result["first"] = self.first

        if self.last:
            result["last"] = self.last

        return result
