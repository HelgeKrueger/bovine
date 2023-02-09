from enum import Enum


class PeerType(Enum):
    TRUSTED = "TRUSTED"
    BLOCKED = "BLOCKED"
    NEW = "NEW"
    OFFLINE = "OFFLINE"
