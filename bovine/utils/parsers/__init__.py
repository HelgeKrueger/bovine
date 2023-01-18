from .signature import Signature


def parse_signature_header(header):
    return Signature.from_signature_header(header)


def parse_account_name(account):
    if account[0] == "@":
        account = account[1:]

    if "@" in account:
        return tuple(account.split("@", 1))
    return account, None
