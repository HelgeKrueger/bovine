class ContextBuilder:
    def __init__(self):
        self.context_list = ["https://www.w3.org/ns/activitystreams"]
        self.additional_contexts = {}

    def add(self, *args, **kwargs):
        self.additional_contexts = {**self.additional_contexts, **kwargs}
        self.context_list += args
        return self

    def absorb(self, obj):
        if not isinstance(obj["@context"], str):
            for item in obj["@context"]:
                if isinstance(item, dict):
                    self.add(**item)
                elif item != "https://www.w3.org/ns/activitystreams":
                    self.context_list.append(item)

        del obj["@context"]

        return obj

    def build(self):
        if len(self.additional_contexts) == 0:
            if len(self.context_list) == 1:
                return self.context_list[0]
            return self.context_list

        return self.context_list + [self.additional_contexts]
