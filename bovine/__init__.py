from .types import LocalUser
from .utils import dump_incoming_inbox_to_stdout, get_server_keys


def get_bovine_user(
    domain: str,
) -> LocalUser:
    server_public_key, server_private_key = get_server_keys()

    url = f"https://{domain}/activitypub/bovine"

    bovine_user = LocalUser(
        "bovine",
        url,
        server_public_key,
        server_private_key,
        "Application",
        no_auth_fetch=True,
    ).add_inbox_processor(dump_incoming_inbox_to_stdout)

    return bovine_user
