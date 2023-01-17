from tortoise.models import Model
from tortoise import fields


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


class InboxEntry(Model):
    id = fields.IntField(pk=True)
    actor = fields.ForeignKeyField("models.Actor", related_name="inbox_entries")
    created = fields.DatetimeField()
    content = fields.JSONField()


class OutboxEntry(Model):
    id = fields.IntField(pk=True)
    actor = fields.ForeignKeyField("models.Actor", related_name="outbox_entries")
    local_path = fields.CharField(max_length=255)
    created = fields.DatetimeField()
    content = fields.JSONField()
