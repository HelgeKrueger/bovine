import os

from bovine_core.utils.crypto import generate_public_private_key


async def dump_incoming_inbox_to_stdout(local_user, result, session):
    result.dump()


def get_server_keys():
    public_key_path = ".files/server_public_key.pem"
    private_key_path = ".files/server_private_key.pem"

    return get_public_private_key_from_files(public_key_path, private_key_path)


def get_public_private_key_from_files(public_key_path, private_key_path):
    public_key = None
    private_key = None

    if os.path.exists(public_key_path):
        with open(public_key_path) as f:
            public_key = f.read()
    if os.path.exists(private_key_path):
        with open(private_key_path) as f:
            private_key = f.read()

    if public_key and private_key:
        return public_key, private_key

    public_key_pem, private_key_pem = generate_public_private_key()

    if not os.path.exists(".files"):
        os.mkdir(".files")

    with open(public_key_path, "w") as f:
        f.write(public_key_pem)

    with open(private_key_path, "w") as f:
        f.write(private_key_pem)

    return public_key_pem, private_key_pem
