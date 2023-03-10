class BaseCountAndItems:
    async def item_count(self, local_user) -> int:
        return 0

    async def items(self, local_user, **kwargs) -> dict | None:
        return {"items": []}
