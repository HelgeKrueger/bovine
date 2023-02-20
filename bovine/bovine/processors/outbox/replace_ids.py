import json

from bovine.types import LocalActor, ProcessingItem


async def replace_ids(item: ProcessingItem, local_actor: LocalActor):
    # FIXME?
    if isinstance(item, dict):
        obj = item
    else:
        obj = item.get_data()

    new_id = None

    if "object" in obj and "id" in obj["object"]:
        new_id = local_actor.generate_uuid()
        obj["object"]["id"] = new_id

    if "id" in obj:
        if new_id:
            # type_string = obj["type"].lower()
            obj["id"] = f"{new_id}/activity"
        else:
            obj["id"] = local_actor.generate_uuid()

    if isinstance(item, dict):
        return item

    item.data = obj
    item.body = json.dumps(obj)

    return item
