from .object_builder import ObjectBuilder


class NoteBuilder(ObjectBuilder):
    def __init__(self, account, content, followers=None):
        super().__init__("Note", account, followers=followers)

        self.with_content(content)
