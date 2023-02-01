from . import get_public_private_key_from_files


def get_user_keys():
    return get_public_private_key_from_files(
        ".files/public_key.pem", ".files/private_key.pem"
    )
