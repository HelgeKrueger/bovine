from .actor_builder import ActorBuilder
from .outbox_builder import OutboxBuilder


def build_actor(actor_name: str, actor_type: str = "Person"):
    return ActorBuilder(actor_name, actor_type=actor_type)


def build_outbox(url: str):
    return OutboxBuilder(url)
