from datetime import datetime
from typing import Set


class NoteBuilder:
    def __init__(self, account: str, url: str, content: str):
        self.account = account
        self.content = content
        self.url = url
        self.to: Set[str] = set()
        self.cc: Set[str] = set()
        self.published = datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
        self.hashtags: Set[str] = set()
        self.mentions: Set[str] = set()
        self.conversation: str | None = None
        self.reply_to_id: str | None = None
        self.reply_to_atom_uri: str | None = None
        self.source: dict | None = None

    def as_public(self, followers=None):
        # FIXME: Broken in the way followers is added
        self.to.add("https://www.w3.org/ns/activitystreams#Public")
        if followers:
            self.cc.add(followers)
        else:
            self.cc.add(f"{self.account}/followers")
        return self

    def add_cc(self, recipient: str):
        self.cc.add(recipient)
        return self

    def add_to(self, recipient: str):
        self.to.add(recipient)
        return self

    def as_unlisted(self):
        self.to.add(f"{self.account}/followers")
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

    def with_reply_to_atom_uri(self, uri: str):
        self.reply_to_atom_uri = uri
        return self

    def with_source(self, content: str, media_type: str):
        self.source = {"content": content, "mediaType": media_type}
        return self

    def build(self) -> dict:
        result: dict = {
            "@context": "https://www.w3.org/ns/activitystreams",
            "id": self.url,
            "attributedTo": self.account,
            "type": "Note",
            "inReplyTo": None,
            "content": self.content,
            "published": self.published,
            "to": list(self.to),
            "cc": list(self.cc - self.to),
        }

        result = self._add_tag(result)

        if self.reply_to_id:
            result["inReplyTo"] = self.reply_to_id

        if self.reply_to_atom_uri:
            result["inReplyToAtomUri"] = self.reply_to_atom_uri

        if self.conversation:
            result["conversation"] = self.conversation

        if self.source:
            result["source"] = self.source

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
