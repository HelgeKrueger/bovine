def actor_for_object(data):
    if "attributedTo" in data:
        return data.get("attributedTo")
    return data.get("actor", "__NO__ACTOR__")


def recipients_for_object(data):
    return set.union(*[set(data.get(key, [])) for key in ["to", "cc"]])


def is_public(data):
    recipients = recipients_for_object(data)

    return any(
        x in recipients
        for x in ["Public", "as:Public", "https://www.w3.org/ns/activitystreams#Public"]
    )
