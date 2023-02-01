from .note_builder import NoteBuilder
from .tombstone_builder import TombstoneBuilder


def build_note(account: str, url: str, content: str) -> NoteBuilder:
    return NoteBuilder(account, url, content)


def tombstone(object_id):
    return TombstoneBuilder(object_id).build()
