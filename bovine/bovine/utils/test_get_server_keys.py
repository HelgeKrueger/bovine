from . import get_server_keys


def test_get_server_keys():
    public_key, private_key = get_server_keys()

    assert public_key
    assert private_key
