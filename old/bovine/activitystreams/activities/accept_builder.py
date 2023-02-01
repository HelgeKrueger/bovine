class AcceptBuilder:
    def __init__(self, account: str, obj: dict):
        self.account = account
        self.obj = obj

    def build(self) -> dict:
        return {
            "@context": "https://www.w3.org/ns/activitystreams",
            "id": self.account + "#accepts/follows/",
            "type": "Accept",
            "actor": self.account,
            "object": self.obj,
        }
