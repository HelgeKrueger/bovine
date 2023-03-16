import logging

from cryptography.hazmat.primitives.asymmetric import ed25519
from multiformats import multibase, multicodec

from .crypto import sign_message, verify_signature
from .crypto.did_key import did_key_to_public_key

logger = logging.getLogger(__name__)


class HttpSignature:
    def __init__(self):
        self.fields = []

    def build_signature(self, key_id, private_key):
        message = self.build_message()

        signature_string = sign_message(private_key, message)
        headers = " ".join(name for name, _ in self.fields)

        signature_parts = [
            f'keyId="{key_id}"',
            'algorithm="rsa-sha256"',  # FIXME: Should other algorithms be supported?
            f'headers="{headers}"',
            f'signature="{signature_string}"',
        ]

        return ",".join(signature_parts)

    def ed25519_sign(self, private_encoded):
        private_bytes = multicodec.unwrap(multibase.decode(private_encoded))[1]
        private_key = ed25519.Ed25519PrivateKey.from_private_bytes(private_bytes)

        message = self.build_message()

        return multibase.encode(private_key.sign(message.encode("utf-8")), "base58btc")

    def ed25519_verify(self, didkey, signature):
        public_key = did_key_to_public_key(didkey)

        signature = multibase.decode(signature)

        message = self.build_message().encode("utf-8")

        return public_key.verify(signature, message)

    def verify(self, public_key, signature):
        message = self.build_message()
        return verify_signature(public_key, message, signature)

    def build_message(self):
        return "\n".join(f"{name}: {value}" for name, value in self.fields)

    def with_field(self, field_name, field_value):
        self.fields.append((field_name, field_value))
        return self
