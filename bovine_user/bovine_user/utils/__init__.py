import tomli_w

from bovine_user.types import EndpointType


def create_toml_file(user):
    account_url = ""
    for endpoint in user.endpoints:
        if endpoint.endpoint_type == EndpointType.ACTOR:
            account_url = endpoint.name

    keypair = user.keypairs[0]

    data = {
        "account_url": account_url,
        "public_key_url": f"{account_url}#{keypair.name}",
        "private_key": keypair.private_key,
    }

    return tomli_w.dumps(data) + "\n"
