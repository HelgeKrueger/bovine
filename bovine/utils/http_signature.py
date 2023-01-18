import logging
from urllib.parse import urlparse

from .crypto import sign_message, verify_signature
from .parsers import parse_signature_header


class HttpSignature:
    def __init__(self):
        self.fields = []

    def build_signature(self, key_id, private_key):
        message = self.build_message()
        signature_string = sign_message(private_key, message)

        headers = " ".join(name for name, _ in self.fields)

        signature_parts = [
            f'keyId="{key_id}"',
            'algorithm="rsa-sha256"',
            f'headers="{headers}"',
            f'signature="{signature_string}"',
        ]

        return ",".join(signature_parts)

    def verify(self, public_key, signature):
        return verify_signature(public_key, self.build_message(), signature)

    def build_message(self):
        return "\n".join(f"{name}: {value}" for name, value in self.fields)

    def with_field(self, field_name, field_value):
        self.fields.append((field_name, field_value))
        return self


class SignatureChecker:
    def __init__(self, key_retriever):
        self.key_retriever = key_retriever

    async def validate_signature(self, request, digest):
        if "signature" not in request.headers:
            return False

        if digest is not None:
            if request.headers["digest"] != digest:
                logging.warn("Different diggest")

        try:
            http_signature = HttpSignature()
            parsed_signature = parse_signature_header(request.headers["signature"])

            for field in parsed_signature.fields():
                if field == "(request-target)":
                    method = request.method.lower()
                    path = urlparse(request.url).path
                    http_signature.with_field(field, f"{method} {path}")
                else:
                    http_signature.with_field(field, request.headers[field])

            public_key = await self.key_retriever(parsed_signature.key_id)

            return http_signature.verify(public_key, parsed_signature.signature)
        except Exception as e:
            print(e)
            return False
