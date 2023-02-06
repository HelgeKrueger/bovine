from pyld import jsonld
import requests
import os
import json
import pytest
from bovine_core.activitystreams import (
    build_actor,
    build_ordered_collection,
    build_ordered_collection_page,
)


def get_json_ld(url):
    if os.path.exists("as.json"):
        with open("as.json") as f:
            return json.load(f)
    asld = requests.get(
        "https://www.w3.org/ns/activitystreams",
        headers={"accept": "application/ld+json"},
    ).json()

    with open("as.json", "w") as f:
        json.dump(asld, f)

    return asld


def activity_provider():
    yield build_actor("actor_name").build()
    yield build_ordered_collection("url").build()


@pytest.mark.parametrize("activity", activity_provider())
def test_json_ld_structure(activity):
    as_ld = get_json_ld("https://www.w3.org/ns/activitystreams")

    def loader(*args, **kwargs):
        return {
            "contentType": "application/ld+json",
            "contextUrl": None,
            "documentUrl": "https://www.w3.org/ns/activitystreams",
            "document": as_ld,
        }

    frame = {
        "@context": "https://www.w3.org/ns/activitystreams",
    }

    jsonld.set_document_loader(loader)

    result = activity
    result = jsonld.frame(result, frame)

    assert result == activity


def test_json_ld_structure_page():
    activity = (
        build_ordered_collection_page("https://url?page", "https://url")
        .with_items([])
        .build()
    )
    as_ld = get_json_ld("https://www.w3.org/ns/activitystreams")

    def loader(*args, **kwargs):
        return {
            "contentType": "application/ld+json",
            "contextUrl": None,
            "documentUrl": "https://www.w3.org/ns/activitystreams",
            "document": as_ld,
        }

    frame = {"@context": "https://www.w3.org/ns/activitystreams", "partOf": {}}

    jsonld.set_document_loader(loader)

    result = activity
    result = jsonld.frame(result, frame)

    assert result == activity
