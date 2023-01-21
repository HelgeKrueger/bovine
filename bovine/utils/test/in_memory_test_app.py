import aiohttp
from unittest.mock import AsyncMock
from quart import Quart

from bovine import get_bovine_user
from bovine.server import default_configuration
from bovine.utils import dump_incoming_inbox_to_stdout
from bovine.utils.in_memory_store import InMemoryUserStore
from bovine.utils.http_signature import SignatureChecker
from bovine.types import LocalUser
from bovine.clients import get_public_key

from . import get_user_keys

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
    }
)
app.register_blueprint(default_configuration)
