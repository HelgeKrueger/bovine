from .types import LocalUser
from .utils import get_server_keys, dump_incoming_inbox_to_stdout


def get_bovine_user(domain):
    server_public_key, server_private_key = get_server_keys()

    url = f"https://{domain}/acitivitypub/bovine"

    bovine_user = LocalUser(
        "bovine", url, server_public_key, server_private_key, "Application"
    ).add_inbox_processor(dump_incoming_inbox_to_stdout)

    return bovine_user
