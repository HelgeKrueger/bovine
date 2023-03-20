class CollectionIterator:
    def __init__(self, collection_helper, max_number):
        self.count = 0
        self.collection_helper = collection_helper
        self.max_number = max_number

    def __aiter__(self):
        return self

    async def __anext__(self):
        self.count += 1
        if self.count > self.max_number:
            raise StopAsyncIteration

        return await self.collection_helper.next_item()
