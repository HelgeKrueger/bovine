import re


def is_activity_request(header):
    if re.match(r"application/activity[+]json", header, re.IGNORECASE):
        return True
    if re.match(
        r'application/ld[+]json; profile="https://www.w3.org/ns/activitystreams"',
        header,
        re.IGNORECASE,
    ):
        return True

    return False
