import logging

from bovine.types import LocalActor

from bovine_tortoise.models import Actor

logger = logging.getLogger(__name__)


class CountAndItems:
    def __init__(self, obj):
        self.obj = obj

    async def item_count(self, local_actor: LocalActor) -> int:
        actor = await Actor.get_or_none(account=local_actor.name)
        if actor is None:
            logger.error("Failed to fetch actor")
            return 0

        return await self.obj.filter(actor=actor).count()

    async def items(self, local_actor: LocalActor, **kwargs) -> dict | None:
        actor = await Actor.get_or_none(account=local_actor.name)
        if actor is None:
            logger.error("Failed to fetch actor")
            return None

        limit = int(kwargs.get("limit", 10))

        query = self.obj.filter(actor=actor)

        if kwargs.get("first"):
            query = query.order_by("-id")

        if kwargs.get("min_id"):
            min_id = int(kwargs.get("min_id"))
            query = query.order_by("-id")
            query = query.filter(id__lt=min_id)
        if kwargs.get("max_id"):
            max_id = int(kwargs.get("max_id"))
            query = query.filter(id__gt=max_id)

        result = await query.limit(limit).all()

        next_prev = {}
        if len(result) > 0:
            min_id = max(x.id for x in result)
            max_id = min(x.id for x in result)
            next_prev = {
                "prev": f"max_id={min_id}",
                "next": f"min_id={max_id}",
            }
        result = sorted(result, key=lambda x: -x.id)

        return {"items": [x.content for x in result], **next_prev}
