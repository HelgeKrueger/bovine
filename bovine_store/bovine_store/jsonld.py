import requests_cache
from pyld import jsonld

requests_cache.install_cache("context_cache")

jsonld.set_document_loader(jsonld.requests_document_loader(timeout=60))


async def split_into_objects(input_data):
    context = input_data["@context"]
    flattened = jsonld.flatten(input_data)
    compacted = jsonld.compact(flattened, context)

    if "@graph" not in compacted:
        return [compacted]

    local, remote = split_remote_local(compacted["@graph"])

    return [frame_object(obj, local, context) for obj in remote]


def frame_object(obj, local, context):
    to_frame = {"@context": context, "@graph": [obj] + local}
    frame = {"@context": context, "id": obj["id"]}
    return jsonld.frame(to_frame, frame)


def split_remote_local(graph):
    local = [x for x in graph if x["id"].startswith("_")]
    remote = [x for x in graph if not x["id"].startswith("_")]

    return local, remote


def combine_items(data, items):
    return frame_object(data, items, data["@context"])
