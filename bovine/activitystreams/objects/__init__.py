from .note_builder import NoteBuilder


def build_note(account: str, url: str, content: str) -> NoteBuilder:
    return NoteBuilder(account, url, content)
