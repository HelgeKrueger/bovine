import uuid


class FollowBuilder:
    def __init__(self, domain: str, actor: str, tofollow: str):
        self.domain = domain
        self.actor = actor
        self.tofollow = tofollow

    def build(self) -> dict:
        uuid_string = str(uuid.uuid4())

        return {
            "@context": "https://www.w3.org/ns/activitystreams",
            "id": f"https://{self.domain}/{uuid_string}",
            "type": "Follow",
            "actor": self.actor,
            "object": self.tofollow,
        }
