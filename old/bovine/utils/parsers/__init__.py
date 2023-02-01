

def parse_account_name(account):
    if account[0] == "@":
        account = account[1:]

    if "@" in account:
        return tuple(account.split("@", 1))
    return account, None
