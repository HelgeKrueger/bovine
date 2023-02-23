import asyncio
import logging


from bovine_store.models import StoredJsonObject


from bovine_store.jsonld import combine_items
from bovine_store.permissions import has_access

logger = logging.getLogger(__name__)


async def retrieve_remote_object(retriever, object_id, include=[]):
    result = await StoredJsonObject.get_or_none(id=object_id).prefetch_related(
        "visible_to"
    )
    if not await has_access(result, retriever):
        return None

    data = result.content
    if len(include) == 0:
        return data

    items = await asyncio.gather(
        *[StoredJsonObject.get_or_none(id=data[key]) for key in include if key in data]
    )
    items = [obj.content for obj in items if obj]

    logger.debug("Retrieved %d items", len(items))

    return combine_items(data, items)
