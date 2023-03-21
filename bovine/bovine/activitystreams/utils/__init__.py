def actor_for_object(data):
    if "attributedTo" in data:
        actor = data.get("attributedTo")
    else:
        actor = data.get("actor")
    actor = id_for_object(actor)

    if actor:
        return actor

    return "__NO__ACTOR__"


def id_for_object(data):
    if data is None:
        return None
    if isinstance(data, str):
        return data
    return data.get("id", None)


def property_for_key_as_set(data, key):
    if data is None:
        return set()
    result = data.get(key, [])
    if isinstance(result, str):
        return set([result])
    return set(result)


def recipients_for_object(data):
    return set.union(
        *[
            property_for_key_as_set(data, key)
            for key in ["to", "cc", "bto", "bcc", "audience"]
        ]
    )


def remove_public(recipients):
    return {
        x
        for x in recipients
        if x
        not in ["Public", "as:Public", "https://www.w3.org/ns/activitystreams#Public"]
    }


def is_public(data):
    recipients = recipients_for_object(data)

    return any(
        x in recipients
        for x in ["Public", "as:Public", "https://www.w3.org/ns/activitystreams#Public"]
    )
