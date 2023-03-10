from .parse import parse_fediverse_handle


def test_parse_fediverse_handle():
    assert parse_fediverse_handle("account") == ("account", None)
    assert parse_fediverse_handle("account@domain") == ("account", "domain")

    assert parse_fediverse_handle("account@domain@@@") == ("account", "domain@@@")
    assert parse_fediverse_handle("@account@domain@@@") == ("account", "domain@@@")
    assert parse_fediverse_handle("@account") == ("account", None)
