import base64
import hashlib

from cryptography.hazmat.primitives.serialization import (
    load_pem_private_key,
    load_pem_public_key,
)
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

from cryptography.exceptions import InvalidSignature


def sign_message(private_key, message):
    key = load_pem_private_key(private_key.encode("utf-8"), password=None)

    return base64.standard_b64encode(
        key.sign(
            message.encode("utf-8"),
            padding.PKCS1v15(),
            hashes.SHA256(),
        )
    ).decode("utf-8")


def verify_signature(public_key, message, signature):
    public_key_loaded = load_pem_public_key(public_key.encode("utf-8"))

    try:
        public_key_loaded.verify(
            base64.standard_b64decode(signature),
            message.encode("utf-8"),
            padding.PKCS1v15(),
            hashes.SHA256(),
        )
    except InvalidSignature:
        return False

    return True


def content_digest_sha256(content):
    if isinstance(content, str):
        content = content.encode("utf-8")

    digest = base64.standard_b64encode(hashlib.sha256(content).digest()).decode("utf-8")
    return "SHA-256=" + digest
