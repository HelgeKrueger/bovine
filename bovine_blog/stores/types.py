from datetime import datetime

from bovine_tortoise.models import OutboxEntry


def extract_content(activity: dict) -> str:
    obj = activity["object"]

    if "content" not in obj or not isinstance(obj["content"], str):
        return "bad input"
    return obj["content"]


def extract_in_reply_to(activity: dict) -> str | None:
    obj = activity["object"]
    if not isinstance(obj["content"], str):
        return None
    return obj.get("inReplyTo", None)


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
        if "/" in entry.local_path:
            author, local_id = entry.local_path.split("/", 1)
        else:
            author = ""
            local_id = entry.local_path
        entry = PostEntry(local_id, author, entry.created, content).set_in_reply_to(
            extract_in_reply_to(entry.content)
        )
        return entry
