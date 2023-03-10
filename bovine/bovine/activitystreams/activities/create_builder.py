from datetime import datetime


class CreateBuilder:
    def __init__(self, obj: dict):
        self.obj = obj
        self.account = self.obj.get("attributedTo", None)
        self.url = self.obj.get("id", None)
        self.to = self.obj.get("to", [])
        self.cc = self.obj.get("cc", [])
        self.published = self.obj.get(
            "published", datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
        )

    def with_account(self, account: str):
        self.account = account
        return self

    def as_public(self):
        self.to.append("https://www.w3.org/ns/activitystreams#Public")
        self.cc.append(f"{self.account}/followers")
        return self

    def as_unlisted(self):
        self.to.append(f"{self.account}/followers")
        self.cc.append("https://www.w3.org/ns/activitystreams#Public")
        return self

    def build(self) -> dict:
        return {
            "@context": [
                "https://www.w3.org/ns/activitystreams",
                {
                    "inReplyToAtomUri": "ostatus:inReplyToAtomUri",
                    "conversation": "ostatus:conversation",
                    "ostatus": "http://ostatus.org#",
                },
            ],
            "id": self.url,
            "type": "Create",
            "actor": self.account,
            "object": self.obj,
            "published": self.published,
            "to": self.to,
            "cc": self.cc,
        }
