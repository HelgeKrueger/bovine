import os
import aiohttp
from quart import Quart

from bovine import get_bovine_user
from bovine.processors.inbox.accept_follow import accept_follow_request
from bovine.server import default_configuration
from bovine.types import LocalActor
from bovine.utils import dump_incoming_inbox_to_stdout
from bovine.utils.in_memory_store import InMemoryUserStore
from bovine.utils.test import get_user_keys
from bovine.processors.processor_list import ProcessorList


async def return_true(*args, **kwargs):
    return True


domain = os.environ.get("DOMAIN", "my_domain")

public_key, private_key = get_user_keys()
local_user = LocalActor(
    "test",
    f"https://{domain}/activitypub/test",
    public_key,
    private_key,
    "Person",
).set_inbox_process(
    ProcessorList().add(accept_follow_request).add(dump_incoming_inbox_to_stdout).apply
)
data_store = InMemoryUserStore()
data_store.add_user(local_user)
data_store.add_user(get_bovine_user(domain))

app = Quart(__name__)


@app.before_serving
async def startup():
    app.config["session"] = aiohttp.ClientSession()


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
