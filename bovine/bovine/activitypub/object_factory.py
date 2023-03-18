from bovine.activitystreams.objects.note_builder import NoteBuilder


class ObjectFactory:
    def __init__(self, actor_information):
        self.information = actor_information

    def note(self, text):
        return NoteBuilder(
            self.information["id"], text, followers=self.information["followers"]
        )
