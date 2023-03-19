from datetime import datetime
from typing import Set


class ObjectBuilder:
    def __init__(self, object_type: str, account: str, followers=None):
        self.type = object_type
        self.account = account
        self.content = None
        self.name = None
        self.summary = None
        self.url = None
        self.to: Set[str] = set()
        self.cc: Set[str] = set()
        self.published = datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
        self.hashtags: Set[str] = set()
        self.mentions: Set[str] = set()
        self.conversation: str | None = None
        self.reply_to_id: str | None = None
        self.source: dict | None = None
        self.followers = followers

    def with_content(self, content: str):
        self.content = content
        return self

    def with_url(self, url: str):
        self.url = url
        return self

    def with_name(self, name: str):
        self.name = name
        return self

    def with_summary(self, summary: str):
        self.summary = summary
        return self

    def as_public(self, followers=None):
        # FIXME: Broken in the way followers is added
        self.to.add("https://www.w3.org/ns/activitystreams#Public")
        if followers:
            self.cc.add(followers)
        elif self.followers:
            self.cc.add(self.followers)
        else:
            raise Exception("Followers unkown")
        return self

    def add_cc(self, recipient: str):
        self.cc.add(recipient)
        return self

    def add_to(self, recipient: str):
        self.to.add(recipient)
        return self

    def as_unlisted(self, followers=None):
        if followers:
            self.cc.add(followers)
        elif self.followers:
            self.cc.add(self.followers)
        else:
            raise Exception("Followers unkown")
        self.cc.add("https://www.w3.org/ns/activitystreams#Public")
        return self

    def with_hashtag(self, hashtag: str):
        self.hashtags.add(hashtag)
        return self

    def with_mention(self, mention: str):
        self.mentions.add(mention)
        self.cc.add(mention)
        return self

    def with_conversation(self, conversation: str):
        self.conversation = conversation
        return self

    def with_reply(self, rid: str):
        self.reply_to_id = rid
        return self

    def with_source(self, content: str, media_type: str):
        self.source = {"content": content, "mediaType": media_type}
        return self

    def build(self) -> dict:
        result: dict = {
            "@context": "https://www.w3.org/ns/activitystreams",
            "attributedTo": self.account,
            "type": "Note",
            "inReplyTo": None,
            "content": self.content,
            "published": self.published,
            "to": list(self.to),
            "cc": list(self.cc - self.to),
        }

        result = self._add_tag(result)

        extra_fields = {
            "inReplyTo": self.reply_to_id,
            "conversation": self.conversation,
            "source": self.source,
            "name": self.name,
        }

        for key, value in extra_fields.items():
            if value:
                result[key] = value

        return result

    def _add_tag(self, result):
        tag_list = [{"name": tag, "type": "Hashtag"} for tag in self.hashtags] + [
            {"href": mention, "name": mention, "type": "Mention"}
            for mention in self.mentions
        ]

        if len(tag_list) > 0:
            result["tag"] = tag_list

        return result

    def with_published(self, published: datetime):
        self.published = published.replace(microsecond=0).isoformat() + "Z"
        return self
