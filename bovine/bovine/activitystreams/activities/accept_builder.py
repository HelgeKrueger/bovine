class AcceptBuilder:
    def __init__(self, actor: str, obj: dict):
        self.actor = actor
        self.obj = obj

    def build(self) -> dict:
        return {
            "@context": "https://www.w3.org/ns/activitystreams",
            "id": self.actor + "#accepts/follows/",
            "type": "Accept",
            "actor": self.actor,
            "object": self.obj,
            "to": [self.determine_to()],
        }

    def determine_to(self) -> str:
        actor = self.obj.get("actor")

        if isinstance(actor, dict):
            actor = actor.get("id")

        return actor
