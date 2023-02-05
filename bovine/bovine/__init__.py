from .types import LocalActor
from .utils import dump_incoming_inbox_to_stdout, get_server_keys


def get_bovine_user(
    domain: str,
) -> LocalActor:
    server_public_key, server_private_key = get_server_keys()

    url = f"https://{domain}/activitypub/bovine"

    bovine_user = LocalActor(
        "bovine",
        url,
        server_public_key,
        server_private_key,
        "Application",
        no_auth_fetch=True,
    ).set_inbox_process(dump_incoming_inbox_to_stdout)

    return bovine_user
