from tortoise import fields
from tortoise.models import Model

from .utils.peer_type import PeerType


class Actor(Model):
    id = fields.IntField(pk=True)
    account = fields.CharField(max_length=255)
    url = fields.CharField(max_length=255)
    actor_type = fields.CharField(max_length=255)
    private_key = fields.TextField()
    public_key = fields.TextField()


class Follower(Model):
    id = fields.IntField(pk=True)
    actor = fields.ForeignKeyField("models.Actor", related_name="followers")

    account = fields.CharField(max_length=255)
    followed_on = fields.DatetimeField()

    inbox = fields.CharField(max_length=255, null=True)
    public_key = fields.TextField(null=True)


class Following(Model):
    id = fields.IntField(pk=True)
    actor = fields.ForeignKeyField("models.Actor", related_name="following")

    account = fields.CharField(max_length=255)
    followed_on = fields.DatetimeField()


class InboxEntry(Model):
    id = fields.IntField(pk=True)
    actor = fields.ForeignKeyField("models.Actor", related_name="inbox_entries")
    created = fields.DatetimeField()
    content = fields.JSONField()

    conversation = fields.CharField(max_length=255, null=True)
    read = fields.BooleanField(default=True)
    content_id = fields.CharField(max_length=255, null=True)


class OutboxEntry(Model):
    id = fields.IntField(pk=True)
    actor = fields.ForeignKeyField("models.Actor", related_name="outbox_entries")
    local_path = fields.CharField(max_length=255)
    created = fields.DatetimeField()
    content = fields.JSONField()
    content_id = fields.CharField(max_length=255, null=True)


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
