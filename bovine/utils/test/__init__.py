from bovine.utils import get_public_private_key_from_files


def remove_domain_from_url(url):
    assert url.startswith("https://my_domain")

    return url[17:]


def get_user_keys():
    return get_public_private_key_from_files(
        ".files/public_key.pem", ".files/private_key.pem"
    )
