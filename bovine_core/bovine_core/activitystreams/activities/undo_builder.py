class UndoBuilder:
    def __init__(self, obj: dict):
        self.obj = obj

    def build(self) -> dict:
        return {
            "@context": "https://www.w3.org/ns/activitystreams",
            "type": "Undo",
            "actor": self.obj["actor"],
            "object": self.obj,
        }
