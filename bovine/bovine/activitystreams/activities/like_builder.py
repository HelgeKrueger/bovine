import uuid

from bovine.activitystreams.common import build_context


class LikeBuilder:
    def __init__(self, account: str, obj: dict):
        self.account = account
        self.obj = obj
        self.content = None
        self.to = set()
        self.cc = set()

    def add_to(self, recipient):
        self.to.add(recipient)
        return self

    def add_cc(self, recipient):
        self.cc.add(recipient)
        return self

    def with_content(self, content):
        self.content = content
        return self

    def build(self) -> dict:
        context = build_context().build()

        result = {
            "@context": context,
            "id": self.account + "#likes+" + str(uuid.uuid4()),
            "type": "Like",
            "actor": self.account,
            "object": self.obj,
        }

        if self.to:
            result["to"] = list(self.to)

        if self.cc:
            result["cc"] = list(self.cc)

        if self.content:
            result["content"] = self.content

        return result
