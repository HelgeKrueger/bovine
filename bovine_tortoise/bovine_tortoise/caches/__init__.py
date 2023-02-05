import aiohttp
from bovine.clients import get_public_key
from bovine.types import LocalActor

from .public_key import PublicKeyCache


def build_public_key_fetcher(session: aiohttp.ClientSession, bovine_user: LocalActor):
    def get_public_key_wrapper(key_id):
        return get_public_key(session, bovine_user, key_id)

    cache = PublicKeyCache(get_public_key_wrapper)

    return cache.get_for_url
