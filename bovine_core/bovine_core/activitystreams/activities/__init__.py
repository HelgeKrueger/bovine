from .accept_builder import AcceptBuilder
from .create_builder import CreateBuilder
from .delete_builder import DeleteBuilder
from .follow_builder import FollowBuilder


def build_follow(domain: str, actor: str, tofollow: str) -> FollowBuilder:
    return FollowBuilder(domain, actor, tofollow)


def build_accept(account: str, obj: dict) -> AcceptBuilder:
    return AcceptBuilder(account, obj)


def build_create(*args) -> CreateBuilder:
    return CreateBuilder(*args)


def build_delete(actor, object_id):
    return DeleteBuilder(actor, object_id)
