from quart import Quart

from bovine.server import default_configuration
from bovine.stores.in_memory import InMemoryUserStore
from bovine.utils import dump_incoming_inbox_to_stdout
from bovine.utils.http_signature import SignatureChecker
from bovine.types import LocalUser
from bovine.clients import get_public_key

from . import get_user_keys


app = Quart(__name__)

signature_checker = SignatureChecker(get_public_key)

app.config.update({"DOMAIN": "my_domain"})
app.config.data_store = InMemoryUserStore()
app.config.validate_signature = signature_checker.validate_signature
public_key, private_key = get_user_keys()

local_user = LocalUser(
    "user",
    "https://my_domain/activitypub/user",
    public_key,
    private_key,
    "Person",
).add_inbox_processor(dump_incoming_inbox_to_stdout)
app.config.data_store.add_user(local_user)

app.register_blueprint(default_configuration)
