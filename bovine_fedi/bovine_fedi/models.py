from tortoise import fields
from tortoise.models import Model

from .utils.peer_type import PeerType


class Peer(Model):
    id = fields.IntField(pk=True)

    domain = fields.CharField(max_length=255)
    peer_type = fields.CharEnumField(PeerType, default=PeerType.NEW)
    software = fields.CharField(max_length=255, null=True)
    version = fields.CharField(max_length=255, null=True)

    created = fields.DatetimeField(auto_now_add=True)
    updated = fields.DatetimeField(null=True)


class PublicKey(Model):
    id = fields.IntField(pk=True)
    url = fields.CharField(max_length=255, unique=True)
    public_key = fields.TextField()


class StoredObject(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, unique=True)
    data = fields.BinaryField()
