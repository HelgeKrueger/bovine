from bovine.test import get_user_keys

from .crypto import sign_message, verify_signature, content_digest_sha256


def test_crypto_sign_verify():
    message = "secret"

    public_key, private_key = get_user_keys()

    signature = sign_message(private_key, message)

    assert verify_signature(public_key, message, signature)


def test_crypto_sign_verify_failure():
    message = "secret"

    public_key, private_key = get_user_keys()

    assert not verify_signature(public_key, message, "")


def test_content_digest_sha256():
    digest = content_digest_sha256("content")

    assert digest.startswith("SHA-256=")
