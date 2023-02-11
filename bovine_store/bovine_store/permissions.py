from .models import VisibilityTypes, CollectionItem


async def has_access(entry, retriever):
    if retriever == entry.owner:
        return True

    if entry.visibility == VisibilityTypes.PUBLIC:
        return True

    await entry.fetch_related("visible_to")

    if any(item.object_id == retriever for item in entry.visible_to):
        return True

    collections = await CollectionItem.filter(object_id=retriever).all()

    collection_ids = [collection.part_of for collection in collections]

    for item in entry.visible_to:
        if item.object_id in collection_ids:
            return True

    return False
