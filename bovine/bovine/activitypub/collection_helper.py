import bleach

from bovine.activitystreams.utils.print import print_activity

from .collection_iterator import CollectionIterator


def short_version_of_object(obj):
    if "object" in obj:
        obj = obj["object"]

    for key in ["name", "summary", "content", "id"]:
        if key in obj and obj[key]:
            return bleach.clean(obj[key], tags=[], strip=True)

    return "--- unknown  ---"


class CollectionHelper:
    def __init__(self, collection_id, actor):
        self.collection_id = collection_id
        self.actor = actor

        self.basic_information = None
        self.items = None
        self.next_items = None
        self.item_index = None

        self.element_cache = {}

    async def refresh(self):
        if self.basic_information is None:
            self.basic_information = await self.actor.get(self.collection_id)

        response = await self.actor.get(self.basic_information["first"])

        self.items = response["orderedItems"]
        self.next_items = response["next"]
        self.item_index = 0

    async def summary(self):
        print()
        print(f"Items loaded {len(self.items)}")
        print()
        for idx, item in enumerate(self.items):
            obj = await self.get_element(item)
            print(f"{idx:4}: {obj.get('type'):10}: {short_version_of_object(obj)[:80]}")

    async def get_element(self, element):
        if not isinstance(element, str):
            return element

        if element in self.element_cache:
            return self.element_cache[element]

        result = await self.actor.proxy_element(element)

        self.element_cache[element] = result

        return result

    async def next_item(self, do_print=False):
        if self.item_index >= len(self.items):
            response = await self.actor.get(self.next_items)
            self.items += response["orderedItems"]
            self.next_items = response["next"]

        result = self.items[self.item_index]
        self.item_index += 1

        result = await self.get_element(result)

        if do_print:
            print_activity(result)

        return result

    def iterate(self, max_number=10):
        return CollectionIterator(self, max_number)
