from bson import ObjectId
from marshmallow import fields, ValidationError


class ObjectIdField(fields.Field):
    """Custom field to validate MongoDB ObjectId."""

    def _deserialize(self, value, attr, data, **kwargs):
        if not ObjectId.is_valid(value):
            raise ValidationError("Invalid ObjectId.")
        return ObjectId(value)

    def _serialize(self, value, attr, obj, **kwargs):
        return str(value)
