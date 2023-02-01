import os

from .crypto import generate_public_private_key
from .http_signature import HttpSignature


def build_signature(host, method, target):
    return (
        HttpSignature()
        .with_field("(request-target)", f"{method} {target}")
        .with_field("host", host)
    )


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
