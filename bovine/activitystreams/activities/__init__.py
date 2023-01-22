from .accept_builder import AcceptBuilder
from .create_builder import CreateBuilder
from .follow_builder import FollowBuilder


def build_follow(domain, actor, tofollow):
    return FollowBuilder(domain, actor, tofollow)


def build_accept(account, obj):
    return AcceptBuilder(account, obj)


def build_create(*args):
    return CreateBuilder(*args)
