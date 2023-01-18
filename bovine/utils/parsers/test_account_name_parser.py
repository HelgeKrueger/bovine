from . import parse_account_name


def test_parse_account_name():
    assert parse_account_name("account") == ("account", None)
    assert parse_account_name("account@domain") == ("account", "domain")

    assert parse_account_name("account@domain@@@") == ("account", "domain@@@")
    assert parse_account_name("@account@domain@@@") == ("account", "domain@@@")
    assert parse_account_name("@account") == ("account", None)
