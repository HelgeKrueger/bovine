from . import build_signature
from .crypto import generate_public_private_key
from .http_signature import HttpSignature


def test_http_signature():
    public_key, private_key = generate_public_private_key()

    http_signature = HttpSignature().with_field("name", "value")

    signature_string = http_signature.build_signature("key_id", private_key)

    key_id, algorithm, headers, signature = signature_string.split(",")

    assert key_id == 'keyId="key_id"'
    assert algorithm == 'algorithm="rsa-sha256"'
    assert headers == 'headers="name"'
    assert signature.startswith("signature=")


def test_build_signature():
    public_key, private_key = generate_public_private_key()

    http_signature = build_signature("host", "method", "target")

    signature_string = http_signature.build_signature("key_id", private_key)

    key_id, algorithm, headers, signature = signature_string.split(",")

    assert key_id == 'keyId="key_id"'
    assert algorithm == 'algorithm="rsa-sha256"'
    assert headers == 'headers="(request-target) host"'
    assert signature.startswith("signature=")
