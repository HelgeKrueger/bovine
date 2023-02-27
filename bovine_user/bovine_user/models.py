from tortoise import fields
from tortoise.models import Model

from .types import EndpointType


class BovineUser(Model):
    id = fields.IntField(pk=True)

    hello_sub = fields.CharField(max_length=255)
    handle_name = fields.CharField(max_length=255, unique=True)

    created = fields.DatetimeField(auto_now_add=True)
    last_sign_in = fields.DatetimeField(auto_now=True)


class BovineUserEndpoint(Model):
    id = fields.IntField(pk=True)

    bovine_user = fields.ForeignKeyField("models.BovineUser", related_name="endpoints")

    endpoint_type = fields.CharEnumField(enum_type=EndpointType)
    stream_name = fields.CharField(max_length=255)
    name = fields.CharField(max_length=255)


class BovineUserProperty(Model):
    id = fields.IntField(pk=True)

    bovine_user = fields.ForeignKeyField("models.BovineUser", related_name="properties")

    name = fields.CharField(max_length=255)
    value = fields.JSONField()


class BovineUserKeyPair(Model):
    id = fields.IntField(pk=True)

    bovine_user = fields.ForeignKeyField("models.BovineUser", related_name="keypairs")

    name = fields.CharField(max_length=255)

    private_key = fields.TextField()
    public_key = fields.TextField()
