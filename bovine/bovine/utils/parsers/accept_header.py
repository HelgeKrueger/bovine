import re


def is_activity_request(header):
    if re.match(r"application/activity[+]json", header, re.IGNORECASE):
        return True
    if re.match(
        r"application/ld[+]json",  # ; profile="https://www.w3.org/ns/activitystreams"',
        # FIXME it seems this is necessary to allow Takahe to interact with me.
        header,
        re.IGNORECASE,
    ):
        return True

    return False
