from .signature_parser import Signature


def test_signature_header_parsing():
    header_string = 'keyId="https://host.user#main-key",algorithm="rsa-sha256",headers="(request-target) host date digest content-type",signature="h...Kg=="'  # noqa E501

    result = Signature.from_signature_header(header_string)

    assert result.key_id == "https://host.user#main-key"
    assert result.algorithm == "rsa-sha256"
    assert result.headers == "(request-target) host date digest content-type"
    assert result.signature == "h...Kg=="
    assert result.fields() == [
        "(request-target)",
        "host",
        "date",
        "digest",
        "content-type",
    ]


def test_signature_header_without_algorithm():
    header_string = 'keyId="https://host.user#main-key",headers="(request-target) host date",signature="stuff="'  # noqa E501

    result = Signature.from_signature_header(header_string)

    assert result.key_id == "https://host.user#main-key"
    assert result.algorithm == "rsa-sha256"
    assert result.headers == "(request-target) host date"
    assert result.signature == "stuff="
    assert result.fields() == [
        "(request-target)",
        "host",
        "date",
    ]
