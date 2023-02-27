from enum import Enum


class EndpointType(Enum):
    ACTOR = "ACTOR"
    INBOX = "INBOX"
    OUTBOX = "OUTBOX"
    FOLLOWERS = "FOLLOWERS"
    FOLLOWING = "FOLLOWING"

    PROXY_URL = "PROXY_URL"
    EVENT_SOURCE = "EVENT_SOURCE"

    COLLECTION = "COLLECTION"
