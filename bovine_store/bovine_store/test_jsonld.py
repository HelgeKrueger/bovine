from .jsonld import split_into_objects


async def test_json_ld_split_one_item():
    first_id = "https://my_domain/first"
    item = {
        "@context": "https://www.w3.org/ns/activitystreams",
        "id": first_id,
        "type": "Create",
    }

    subobjects = await split_into_objects(item)

    assert subobjects == [item]


async def test_json_ld_split():
    first_id = "https://my_domain/first"
    second_id = "https://my_domain/second"
    item = {
        "@context": "https://www.w3.org/ns/activitystreams",
        "id": first_id,
        "type": "Create",
        "object": {
            "type": "Note",
            "id": second_id,
        },
    }

    subobjects = await split_into_objects(item)

    first, second = subobjects
    assert first["id"] == first_id
    assert second["id"] == second_id

    assert first["object"] == second_id


async def test_json_ld_split_subobject():
    first_id = "https://my_domain/first"
    second_id = "https://my_domain/second"
    item = {
        "@context": "https://www.w3.org/ns/activitystreams",
        "id": first_id,
        "type": "Create",
        "object": {
            "type": "Note",
            "id": second_id,
        },
        "tag": [{"type": "Mention"}],
    }

    subobjects = await split_into_objects(item)

    first, second = subobjects
    assert first["id"] == first_id
    assert second["id"] == second_id

    assert first["object"] == second_id
    assert first["tag"] == {"type": "Mention"}


async def test_json_ld_split_subobject_list():
    first_id = "https://my_domain/first"
    second_id = "https://my_domain/second"
    tags = [{"type": "Mention", "name": "one"}, {"type": "Mention", "name": "two"}]
    item = {
        "@context": "https://www.w3.org/ns/activitystreams",
        "id": first_id,
        "type": "Create",
        "object": {
            "type": "Note",
            "id": second_id,
        },
        "tag": tags,
    }

    subobjects = await split_into_objects(item)

    first, second = subobjects
    assert first["id"] == first_id
    assert second["id"] == second_id

    assert first["object"] == second_id
    assert first["tag"] == tags
