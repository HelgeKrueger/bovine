from bovine.activitystreams.objects.note_builder import NoteBuilder
from bovine.activitystreams.objects.object_builder import ObjectBuilder


class ObjectFactory:
    def __init__(self, actor_information):
        self.information = actor_information

    def note(self, text):
        return NoteBuilder(
            self.information["id"], text, followers=self.information["followers"]
        )

    def article(self):
        return ObjectBuilder(
            "Article", self.information["id"], followers=self.information["followers"]
        )
