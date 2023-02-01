from datetime import datetime


class NoteBuilder:
    def __init__(self, account: str, url: str, content: str):
        self.account = account
        self.content = content
        self.url = url
        self.to = set()
        self.cc = set()
        self.published = datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
        self.hashtags = set()
        self.mentions = set()
        self.conversation = None
        self.reply_to_id = None
        self.reply_to_atom_uri = None
        self.source = None

    def as_public(self):
        self.to.add("https://www.w3.org/ns/activitystreams#Public")
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
        result = {
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

        if len(self.hashtags) > 0:
            if "tag" not in result:
                result["tag"] = []
            result["tag"] += [{"name": tag, "type": "Hashtag"} for tag in self.hashtags]

        if len(self.mentions) > 0:
            if "tag" not in result:
                result["tag"] = []
            result["tag"] += [
                {"href": mention, "name": mention, "type": "Mention"}
                for mention in self.mentions
            ]

        if self.reply_to_id:
            result["inReplyTo"] = self.reply_to_id

        if self.reply_to_atom_uri:
            result["inReplyToAtomUri"] = self.reply_to_atom_uri

        if self.conversation:
            result["conversation"] = self.conversation

        if self.source:
            result["source"] = self.source

        return result

    def with_published(self, published: datetime):
        self.published = published.replace(microsecond=0).isoformat() + "Z"
        return self
