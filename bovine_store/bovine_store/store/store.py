import asyncio
import logging

from bovine_store.jsonld import split_into_objects
from bovine_store.models import StoredJsonObject, VisibilityTypes, VisibleTo


logger = logging.getLogger(__name__)


def should_store(obj):
    if "type" not in obj:
        return True

    if obj["type"] in [
        "Collection",
        "OrderedCollection",
        "CollectionPage",
        "OrderedCollectionPage",
    ]:
        return False

    return True


async def store_remote_object(owner, item, as_public=False, visible_to=[]):
    visibility_type = VisibilityTypes.RESTRICTED
    if as_public:
        visibility_type = VisibilityTypes.PUBLIC

    to_store = await split_into_objects(item)

    tasks = [
        StoredJsonObject.get_or_create(
            id=obj["id"],
            defaults={
                "content": obj,
                "owner": owner,
                "visibility": visibility_type,
            },
        )
        for obj in to_store
        if should_store(obj)
    ]

    id_to_store = {obj["id"]: obj for obj in to_store}

    items = await asyncio.gather(*tasks)

    if visibility_type == VisibilityTypes.PUBLIC:
        for x, c in items:
            x.visibility = VisibilityTypes.PUBLIC
            await x.save()

        return items

    for item, created in items:
        visible_tasks = [
            VisibleTo.get_or_create(
                main_object=item,
                object_id=actor,
            )
            for actor in visible_to
        ]
        await asyncio.gather(*visible_tasks)
        if not created:
            if item.owner == owner:
                item.content = id_to_store[item.id]
                await item.save()

                # FIXME visibility not changed; check timestamps?

    return items
