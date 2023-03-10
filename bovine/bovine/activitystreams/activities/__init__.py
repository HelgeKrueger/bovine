from .accept_builder import AcceptBuilder
from .create_builder import CreateBuilder
from .delete_builder import DeleteBuilder
from .follow_builder import FollowBuilder
from .like_builder import LikeBuilder
from .undo_builder import UndoBuilder


def build_follow(domain: str, actor: str, tofollow: str) -> FollowBuilder:
    return FollowBuilder(domain, actor, tofollow)


def build_accept(account: str, obj: dict) -> AcceptBuilder:
    return AcceptBuilder(account, obj)


def build_create(*args) -> CreateBuilder:
    return CreateBuilder(*args)


def build_delete(actor, object_id):
    return DeleteBuilder(actor, object_id)


def build_like(actor, object_id):
    return LikeBuilder(actor, object_id)


def build_undo(obj: dict) -> UndoBuilder:
    return UndoBuilder(obj)
