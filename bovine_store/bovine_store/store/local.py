import asyncio
import logging
import uuid

from bovine_store.jsonld import split_into_objects
from bovine_store.models import StoredJsonObject, VisibilityTypes, VisibleTo

logger = logging.getLogger(__name__)


async def default_id_generator():
    return "local://" + str(uuid.uuid4())


async def store_local_object(
    owner, item, as_public=False, visible_to=[], id_generator=default_id_generator
):
    logger.info(id_generator)

    visibility_type = VisibilityTypes.RESTRICTED
    if as_public:
        visibility_type = VisibilityTypes.PUBLIC

    split_objects = await split_into_objects(item)

    tasks = [
        StoredJsonObject.get_or_none(
            id=obj["id"],
        )
        for obj in split_objects
    ]
    items_in_database = await asyncio.gather(*tasks)
    ids_in_database = [x.id for x in items_in_database if x]

    to_store = []

    for x in split_objects:
        if x["id"] in ids_in_database:
            to_store.append(x)
        else:
            x["id"] = await id_generator()
            to_store.append(x)

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
    ]

    id_to_store = {obj["id"]: obj for obj in to_store}

    items = await asyncio.gather(*tasks)

    if visibility_type == VisibilityTypes.PUBLIC:
        return [x[0].content for x in items]

    for item, created in items:
        if created:
            visible_tasks = [
                VisibleTo.create(
                    main_object=item,
                    object_id=actor,
                )
                for actor in visible_to
            ]
            await asyncio.gather(*visible_tasks)
        else:
            if item.owner == owner:
                item.content = id_to_store[item.id]
                await item.save()

                # FIXME visibility not changed; check timestamps?

    return [x[0].content for x in items]
