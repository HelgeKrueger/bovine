from quart import Quart

from bovine.server import default_configuration
from bovine.stores.in_memory import InMemoryUserStore
from bovine.utils import dump_incoming_inbox_to_stdout
from bovine.stores import LocalUser

from . import get_user_keys


app = Quart(__name__)

app.config.update({"DOMAIN": "my_domain"})
app.config.data_store = InMemoryUserStore()

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
