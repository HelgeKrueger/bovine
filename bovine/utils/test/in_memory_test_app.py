from unittest.mock import AsyncMock

import aiohttp
from quart import Quart

from bovine import get_bovine_user
from bovine.clients import get_public_key
from bovine.server import default_configuration
from bovine.types import LocalUser
from bovine.utils import dump_incoming_inbox_to_stdout
from bovine.utils.http_signature import SignatureChecker
from bovine.utils.in_memory_store import InMemoryUserStore

from . import get_user_keys


async def silly(*args):
    print("Coroutine silly called with", args)
    return


signature_checker = SignatureChecker(get_public_key)

public_key, private_key = get_user_keys()
local_user = LocalUser(
    "user",
    "https://my_domain/activitypub/user",
    public_key,
    private_key,
    "Person",
).add_inbox_processor(dump_incoming_inbox_to_stdout)

data_store = InMemoryUserStore()
data_store.add_user(local_user)
data_store.add_user(get_bovine_user("my_domain"))

app = Quart(__name__)
app.config.update(
    {
        "DOMAIN": "my_domain",
        "validate_signature": signature_checker.validate_signature,
        "get_user": data_store.get_user,
        "session": AsyncMock(aiohttp.ClientSession),
        "inbox_getter": silly,
    }
)
app.register_blueprint(default_configuration)
