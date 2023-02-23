def actor_for_object(data):
    return data.get("actor", "__NO__ACTOR__")


def recipients_for_object(data):
    return set.union(*[set(data.get(key, [])) for key in ["to", "cc"]])