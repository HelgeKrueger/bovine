from enum import Enum

from tortoise import fields
from tortoise.models import Model


class VisibilityTypes(Enum):
    PUBLIC = "PUBLIC"
    RESTRICTED = "RESTRICTED"


class ObjectType(Enum):
    ACTOR = "ACTOR"
    COLLECTION = "COLLECTION"

    LOCAL = "LOCAL"
    LOCAL_COLLECTION = "LOCAL_COLLECTION"

    REMOTE = "REMOTE"
    REMOTE_COLLECTION = "REMOTE_COLLECTION"


class StoredObject(Model):
    id = fields.CharField(max_length=255, pk=True)
    owner = fields.CharField(max_length=255)

    content = fields.JSONField()
    created = fields.DatetimeField(auto_now_add=True)
    updated = fields.DatetimeField(auto_now=True)

    visibility = fields.CharEnumField(
        VisibilityTypes, default=VisibilityTypes.RESTRICTED
    )
    object_type = fields.CharEnumField(ObjectType, default=ObjectType.LOCAL)


class VisibleTo(Model):
    main_object = fields.ForeignKeyField(
        "models.StoredObject", related_name="visible_to"
    )
    object_id = fields.CharField(max_length=255)


class CollectionItem(Model):
    part_of = fields.CharField(max_length=255)
    object_id = fields.CharField(max_length=255)

    created = fields.DatetimeField(auto_now_add=True)
    updated = fields.DatetimeField(auto_now=True)
