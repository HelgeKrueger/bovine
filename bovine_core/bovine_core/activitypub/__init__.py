from .actor import ActivityPubActor


def actor_from_file(filename, session):
    return ActivityPubActor.from_file(filename, session)
