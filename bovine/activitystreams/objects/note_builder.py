from datetime import datetime


class NoteBuilder:
    def __init__(self, account, url, content):
        self.account = account
        self.content = content
        self.url = url
        self.to = []
        self.cc = []
        self.published = datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

    def as_public(self):
        self.to.append("https://www.w3.org/ns/activitystreams#Public")
        self.cc.append(f"{self.account}/followers")
        return self

    def as_unlisted(self):
        self.to.append(f"{self.account}/followers")
        self.cc.append("https://www.w3.org/ns/activitystreams#Public")
        return self

    def build(self):
        return {
            "@context": "https://www.w3.org/ns/activitystreams",
            "id": self.url,
            "attributedTo": self.account,
            "type": "Note",
            "inReplyTo": None,
            "content": self.content,
            "published": self.published,
            "to": self.to,
            "cc": self.cc,
        }
