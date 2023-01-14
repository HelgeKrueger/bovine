from .follow_builder import FollowBuilder
from .accept_builder import AcceptBuilder


def build_follow(domain, actor, tofollow):
    return FollowBuilder(domain, actor, tofollow)


def build_accept(account, obj):
    return AcceptBuilder(account, obj)
