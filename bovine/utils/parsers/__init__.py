from .signature import Signature


def parse_signature_header(header):
    return Signature.from_signature_header(header)
