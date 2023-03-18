from .note_builder import NoteBuilder
from .tombstone_builder import TombstoneBuilder


def build_note(account: str, url: str, content: str) -> NoteBuilder:
    return NoteBuilder(account, content, followers=f"{account}/followers")


def tombstone(object_id):
    return TombstoneBuilder(object_id).build()
