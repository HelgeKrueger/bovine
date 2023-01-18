from .http_signature import HttpSignature


def build_signature(host, method, target):
    return (
        HttpSignature()
        .with_field("(request-target)", f"{method} {target}")
        .with_field("host", host)
    )


async def dump_incoming_inbox_to_stdout(local_user, result):
    result.dump()
