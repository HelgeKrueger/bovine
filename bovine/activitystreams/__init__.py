from .actor_builder import ActorBuilder
from .outbox_builder import OutboxBuilder


def build_actor(actor_name, actor_type="Person"):
    return ActorBuilder(actor_name, actor_type=actor_type)


def build_outbox(url):
    return OutboxBuilder(url)
