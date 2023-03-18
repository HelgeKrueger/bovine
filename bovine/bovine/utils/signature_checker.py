import logging
import traceback
from urllib.parse import urlparse

from .date import check_max_offset_now, parse_gmt
from .http_signature import HttpSignature
from .signature_parser import parse_signature_header

logger = logging.getLogger(__name__)


class SignatureChecker:
    def __init__(self, key_retriever):
        self.key_retriever = key_retriever

    async def validate_signature(self, request, digest=None):
        if "signature" not in request.headers:
            logger.warning("Signature not present")
            return None

        if digest is not None:
            request_digest = request.headers["digest"]
            request_digest = request_digest[:4].lower() + request_digest[4:]
            if request_digest != digest:
                logger.warning("Different digest")
                return None

        try:
            http_signature = HttpSignature()
            parsed_signature = parse_signature_header(request.headers["signature"])
            signature_fields = parsed_signature.fields()

            if (
                "(request-target)" not in signature_fields
                or "date" not in signature_fields
            ):
                logger.warning("Required field not present in signature")
                return None

            if digest is not None and "digest" not in signature_fields:
                logger.warning("Digest not present, but computable")
                return None

            http_date = parse_gmt(request.headers["date"])
            if not check_max_offset_now(http_date):
                logger.warning(
                    f"Encountered invalid http date {request.headers['date']}"
                )
                return None

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
                logger.warning(f"Could not retrieve key from {parsed_signature.key_id}")
                return None

            if http_signature.verify(public_key, parsed_signature.signature):
                return parsed_signature.key_id

        except Exception as e:
            logger.error(str(e))
            logger.error(request.headers)
            for log_line in traceback.format_exc().splitlines():
                logger.error(log_line)
            return None
