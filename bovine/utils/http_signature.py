import logging
import traceback
from urllib.parse import urlparse

from .crypto import sign_message, verify_signature
from .date import check_max_offset_now, parse_gmt
from .parsers import parse_signature_header

logger = logging.getLogger("http-sig")


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


class SignatureChecker:
    def __init__(self, key_retriever):
        self.key_retriever = key_retriever

    async def validate_signature(self, request, digest=None) -> str | None:
        if "signature" not in request.headers:
            logger.warning("Signature not present")
            return

        if digest is not None:
            if request.headers["digest"] != digest:
                logger.warning("Different diggest")
                return

        try:
            http_signature = HttpSignature()
            parsed_signature = parse_signature_header(request.headers["signature"])
            signature_fields = parsed_signature.fields()

            if (
                "(request-target)" not in signature_fields
                or "date" not in signature_fields
            ):
                logger.warning("Required field not present in signature")
                return

            if digest is not None and "digest" not in signature_fields:
                logger.warning("Digest not present, but computable")
                return

            http_date = parse_gmt(request.headers["date"])
            if not check_max_offset_now(http_date):
                logger.warning(
                    f"Encountered invalid http date {request.headers['date']}"
                )
                return

            for field in signature_fields:
                if field == "(request-target)":
                    method = request.method.lower()
                    parsed_url = urlparse(request.url)
                    path = parsed_url.path
                    http_signature.with_field(field, f"{method} {path}")
                else:
                    http_signature.with_field(field, request.headers[field])

            public_key = await self.key_retriever(parsed_signature.key_id)

            if public_key is None:
                logger.warn(f"Could not retrieve key from {parsed_signature.key_id}")
                return

            if http_signature.verify(public_key, parsed_signature.signature):
                return parsed_signature.key_id
        except Exception as e:
            logger.error(str(e))
            for log_line in traceback.format_exc().splitlines():
                logger.error(log_line)
            return
