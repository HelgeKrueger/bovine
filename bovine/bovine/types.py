import logging
import re
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class Visibility(Enum):
    WEB = "WEB"
    PUBLIC = "PUBLIC"
    RESTRICTED = "RESTRICTED"
    OWNER = "OWNER"


sse_line_pattern = re.compile("(?P<name>[^:]*):?( ?(?P<value>.*))?")


@dataclass
class ServerSentEvent:
    data: str
    event: str | None = None
    id: int | None = None
    retry: int | None = None

    def encode(self) -> bytes:
        message = f"data: {self.data}"
        if self.event is not None:
            message = f"{message}\nevent: {self.event}"
        if self.id is not None:
            message = f"{message}\nid: {self.id}"
        if self.retry is not None:
            message = f"{message}\nretry: {self.retry}"
        message = f"{message}\n\n"
        return message.encode("utf-8")

    @staticmethod
    def parse(raw):
        return ServerSentEvent.parse_utf8(raw.decode("utf-8"))

    @staticmethod
    def parse_utf8(raw):
        data = None
        event = None
        event_id = None
        retry = None
        for line in raw.splitlines():
            m = sse_line_pattern.match(line)
            if m is None:
                logger.warning(f"Invalid Server Sent Event line: '{line}'")
                continue

            name = m.group("name")
            if name == "":
                continue

            value = m.group("value")

            if name == "data":
                if data:
                    data = f"{data}\n{value}"
                else:
                    data = value
            elif name == "event":
                event = value
            elif name == "id":
                event_id = value
            elif name == "retry":
                retry = int(value)

        return ServerSentEvent(data, event, event_id, retry)
