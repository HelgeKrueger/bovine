from bovine.activitystreams.activities import build_create


class ActivityFactory:
    def __init__(self, actor_information):
        self.information = actor_information

    def create(self, note):
        return build_create(note)
