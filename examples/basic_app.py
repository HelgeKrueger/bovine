import os

from quart import Quart

from bovine import get_bovine_user
from bovine.processors.accept_follow import accept_follow_request
from bovine.server import default_configuration
from bovine.types import LocalUser
from bovine.utils import dump_incoming_inbox_to_stdout
from bovine.utils.in_memory_store import InMemoryUserStore
from bovine.utils.test import get_user_keys


async def return_true(*args, **kwargs):
    return True


domain = os.environ.get("DOMAIN", "my_domain")

public_key, private_key = get_user_keys()
local_user = (
    LocalUser(
        "test",
        f"https://{domain}/activitypub/test",
        public_key,
        private_key,
        "Person",
    )
    .add_inbox_processor(accept_follow_request)
    .add_inbox_processor(dump_incoming_inbox_to_stdout)
)
data_store = InMemoryUserStore()
data_store.add_user(local_user)
data_store.add_user(get_bovine_user(domain))

app = Quart(__name__)

app.config.update(
    {
        "DOMAIN": domain,
        "validate_signature": return_true,
        "get_user": data_store.get_user,
    }
)
app.register_blueprint(default_configuration)


if __name__ == "__main__":
    app.run()
