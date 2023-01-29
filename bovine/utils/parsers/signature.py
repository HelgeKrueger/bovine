import logging

logger = logging.getLogger("sig")


class Signature:
    def __init__(self, key_id, algorithm, headers, signature):
        self.key_id = key_id
        self.algorithm = algorithm
        self.headers = headers
        self.signature = signature

        if self.algorithm != "rsa-sha256":
            logger.error(f"Unsupported algorithm {self.algorithm}")

    def fields(self):
        return self.headers.split(" ")

    @staticmethod
    def from_signature_header(header):
        try:
            headers = header.split(",")
            headers = [x.split('="', 1) for x in headers]
            parsed = {x[0]: x[1].replace('"', "") for x in headers}

            return Signature(
                parsed["keyId"],
                parsed["algorithm"],
                parsed["headers"],
                parsed["signature"],
            )
        except Exception:
            logger.error(f"failed to parse signature {header}")
