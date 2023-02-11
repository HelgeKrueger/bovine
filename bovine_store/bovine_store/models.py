from enum import Enum

from tortoise import fields
from tortoise.models import Model


class VisibilityTypes(Enum):
    PUBLIC = "PUBLIC"
    RESTRICTED = "RESTRICTED"


class ObjectType(Enum):
    NORMAL = "NORMAL"
    COLLECTION = "COLLECTION"


class OriginType(Enum):
    LOCAL = "LOCAL"
    REMOTE = "REMOTE"


class StoredObject(Model):
    id = fields.CharField(max_length=255, pk=True)
    owner = fields.CharField(max_length=255)

    content = fields.JSONField()
    created = fields.DatetimeField(auto_now_add=True)
    updated = fields.DatetimeField(auto_now=True)

    origin = fields.CharEnumField(OriginType, default=OriginType.LOCAL)
    visibility = fields.CharEnumField(
        VisibilityTypes, default=VisibilityTypes.RESTRICTED
    )
    object_type = fields.CharEnumField(ObjectType, default=ObjectType.NORMAL)


class VisibleTo(Model):
    main_object = fields.ForeignKeyField("models.StoredObject")
    object_id = fields.CharField(max_length=255)
    object_type = fields.CharEnumField(ObjectType)


class CollectionItem(Model):
    part_of = fields.ForeignKeyField("models.StoredObject")
    object_id = fields.CharField(max_length=255)
