from .actor_builder import ActorBuilder
from .ordered_collection_builder import OrderedCollectionBuilder
from .ordered_collection_page_builder import OrderedCollectionPageBuilder


def build_actor(actor_name: str, actor_type: str = "Person"):
    return ActorBuilder(actor_name, actor_type=actor_type)


def build_ordered_collection(url: str):
    return OrderedCollectionBuilder(url)


def build_ordered_collection_page(url: str, part_of: str):
    return OrderedCollectionPageBuilder(url, part_of)
