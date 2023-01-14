class AcceptBuilder:
    def __init__(self, account, obj):
        self.account = account
        self.obj = obj

    def build(self):
        return {
            "@context": "https://www.w3.org/ns/activitystreams",
            "id": self.account + "#accepts/follows/",
            "type": "Accept",
            "actor": self.account,
            "object": self.obj,
        }
