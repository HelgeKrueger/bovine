import os

from quart import Quart

from bovine.server import default_configuration
from bovine.types import LocalUser
from bovine.stores.in_memory import InMemoryUserStore
from bovine.utils.test import get_user_keys
from bovine.utils import dump_incoming_inbox_to_stdout
from bovine.processors.verify_inbox import verify_inbox_request
from bovine.processors.accept_follow import accept_follow_request


app = Quart(__name__)

domain = os.environ["DOMAIN"]

app.config.update(
    {
        "DOMAIN": domain,
    }
)
app.config.data_store = InMemoryUserStore()
public_key, private_key = get_user_keys()
local_user = (
    LocalUser(
        "test",
        f"https://{domain}/activitypub/test",
        public_key,
        private_key,
        "Person",
    )
    .add_inbox_processor(verify_inbox_request)
    .add_inbox_processor(accept_follow_request)
    .add_inbox_processor(dump_incoming_inbox_to_stdout)
)
app.config.data_store.add_user(local_user)

app.register_blueprint(default_configuration)
