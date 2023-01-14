from .signature import Signature


def test_signature_header_parsing():
    header_string = 'keyId="https://host.user#main-key",algorithm="rsa-sha256",headers="(request-target) host date digest content-type",signature="h...Kg=="'

    result = Signature.from_signature_header(header_string)

    assert result.key_id == "https://host.user#main-key"
    assert result.algorithm == "rsa-sha256"
    assert result.headers == "(request-target) host date digest content-type"
    assert result.signature == "h...Kg=="
