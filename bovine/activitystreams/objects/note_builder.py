from datetime import datetime


class NoteBuilder:
    def __init__(self, account, url, content):
        self.account = account
        self.content = content
        self.url = url
        self.to = []
        self.cc = []
        self.published = datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
        self.hashtags = []
        self.conversation = None
        self.reply_to_id = None
        self.reply_to_atom_uri = None

    def as_public(self):
        self.to.append("https://www.w3.org/ns/activitystreams#Public")
        self.cc.append(f"{self.account}/followers")
        return self

    def add_cc(self, recipient):
        self.cc.append(recipient)
        return self

    def as_unlisted(self):
        self.to.append(f"{self.account}/followers")
        self.cc.append("https://www.w3.org/ns/activitystreams#Public")
        return self

    def with_hashtag(self, hashtag):
        self.hashtags.append(hashtag)
        return self

    def with_conversation(self, conversation):
        self.conversation = conversation
        return self

    def with_reply(self, rid):
        self.reply_to_id = rid
        return self

    def with_reply_to_atom_uri(self, uri):
        self.reply_to_atom_uri = uri
        return self

    def build(self):
        result = {
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

        if len(self.hashtags) > 0:
            if "tag" not in result:
                result["tag"] = []
            result["tag"] += [{"name": tag, "type": "Hashtag"} for tag in self.hashtags]

        if self.reply_to_id:
            result["inReplyTo"] = self.reply_to_id

        if self.reply_to_atom_uri:
            result["inReplyToAtomUri"] = self.reply_to_atom_uri

        if self.conversation:
            result["conversation"] = self.conversation

        return result
