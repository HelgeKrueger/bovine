from .note_builder import NoteBuilder


def build_note(account, url, content):
    return NoteBuilder(account, url, content)
