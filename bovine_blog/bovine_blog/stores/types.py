import re
from datetime import datetime

from bovine_tortoise.models import OutboxEntry


def extract_content(activity: dict) -> str:
    try:
        obj = activity.get("object", None)

        if "content" not in obj or not isinstance(obj["content"], str):
            return "bad input"
        return obj["content"]
    except Exception:
        return "bad input"


def extract_in_reply_to(activity: dict) -> str | None:
    try:
        obj = activity.get("object", "not found")
        if not isinstance(obj["content"], str):
            return None
        return obj.get("inReplyTo", None)
    except Exception:
        return None


class PostEntry:
    def __init__(self, local_id: str, author: str, published: datetime, content: str):
        self.author = author
        self.local_id = local_id
        self.published = published
        self.content = content
        self.in_reply_to = None

    def build_link(self) -> str:
        return f"/{self.author}/{self.local_id}"

    def build_published(self) -> str:
        return self.published.strftime("%Y-%m-%d %H:%M:%S")

    def set_in_reply_to(self, in_reply_to):
        self.in_reply_to = in_reply_to
        return self

    def as_dict(self) -> dict:
        return {
            "author": self.author,
            "link": self.build_link(),
            "published": self.build_published(),
            "content": self.content,
            "in_reply_to": self.in_reply_to,
        }

    @staticmethod
    def from_outbox_entry(entry: OutboxEntry):
        content = extract_content(entry.content)

        print(entry.local_path)

        re_match = re.search(
            r"([^/]*)/([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})",
            entry.local_path,
        )

        if not re_match:
            author = ""
            local_id = entry.local_path
        else:
            author = re_match.group(1)
            local_id = re_match.group(2)

        entry = PostEntry(local_id, author, entry.created, content).set_in_reply_to(
            extract_in_reply_to(entry.content)
        )
        return entry
