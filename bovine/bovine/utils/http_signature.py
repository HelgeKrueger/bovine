import logging

from .crypto import sign_message, verify_signature

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

    def verify(self, public_key, signature):
        message = self.build_message()
        return verify_signature(public_key, message, signature)

    def build_message(self):
        return "\n".join(f"{name}: {value}" for name, value in self.fields)

    def with_field(self, field_name, field_value):
        self.fields.append((field_name, field_value))
        return self
