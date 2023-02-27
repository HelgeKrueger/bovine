from bovine_core.types import Visibility

from .common import build_context


class ActorBuilder:
    def __init__(self, name: str, actor_type: str = "Person"):
        self.name = name
        self.actor_type = actor_type
        self.account_url: str | None = None
        self.public_key: str | None = None
        self.public_key_name: str | None = None
        self.context_builder = build_context()

    def with_account_url(self, account_url: str):
        self.account_url = account_url
        self.inbox = self.account_url + "/inbox"
        self.outbox = self.account_url + "/outbox"
        self.event_source = self.account_url + "/serverSentEvents"
        return self

    def with_inbox(self, inbox: str):
        self.inbox = inbox
        return self

    def with_outbox(self, outbox: str):
        self.outbox = outbox
        return self

    def with_event_source(self, event_source):
        self.event_source = event_source
        return self

    def with_public_key(self, public_key: str, key_name: str = "main-key"):
        self.public_key = public_key
        self.public_key_name = key_name
        self.context_builder.add("https://w3id.org/security/v1")
        return self

    def build(self, visibility=Visibility.PUBLIC):
        return {
            "@context": self.context_builder.build(),
            "name": self.name,
            "preferredUsername": self.name,
            "type": self.actor_type,
            **self._build_account_urls(visibility),
            **self._build_private_key(),
        }

    def _build_context(self):
        if self.public_key:
            return [
                "https://www.w3.org/ns/activitystreams",
                "https://w3id.org/security/v1",
            ]

        return "https://www.w3.org/ns/activitystreams"

    def _build_account_urls(self, visibility):
        if not self.account_url:
            return {}

        if visibility == Visibility.WEB:
            return {"id": self.account_url}

        result = {
            "id": self.account_url,
            "inbox": self.inbox,
            "outbox": self.outbox,
        }

        if visibility == Visibility.OWNER:
            result["endpoints"] = {"eventSource": self.event_source}

        return result

    def _build_private_key(self):
        if self.public_key:
            return {
                "publicKey": {
                    "id": f"{self.account_url}#{self.public_key_name}",
                    "owner": self.account_url,
                    "publicKeyPem": self.public_key,
                }
            }
        return {}
