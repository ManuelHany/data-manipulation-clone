from marshmallow import Schema, fields, validate, validates, ValidationError, post_load, pre_load
import os
from flask import request
from flask_jwt_extended import get_jwt_identity

from common.rgb import get_file_from_server
from common.custom_fields import ObjectIdField
from common.file_types import (
    PICTURE_EXTENSIONS,
    TABULAR_DATA_EXTENSIONS,
    TEXTUAL_DATA_EXTENSIONS
)
from constants import (
    EMAIL_ALREADY_EXISTS_KEY,
    USER_NOT_EXISTS_KEY,
    CODE_ALREADY_EXISTS_KEY,
)
from models.files import FilesModel


class HistogramGenerationSchema(Schema):
    image_name = fields.String(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_id = None
        self.image_path = None

    @pre_load()
    def process_fields(self, data, **kwargs):
        self.user_id = get_jwt_identity()
        return data

    @validates("image_name")
    def validate_image_name(self, image_name):
        user_id = self.user_id
        image_document = RgbDBValidator.validate_image_name(user_id, image_name)
        self.image_path = image_document['file_path']

    @post_load
    def include_additional_fields(self, data, **kwargs):
        data['user_id'] = self.user_id
        data['image_path'] = self.image_path
        return data


class MaskGenerationSchema(HistogramGenerationSchema):
    mask_type = fields.Str(
        required=True,
        validate=validate.OneOf(["bitwise_and", "bitwise_or", "bitwise_xor", "bitwise_not"])
    )
    hue_lower = fields.Integer(
        required=True,
        validate=validate.Range(min=0, max=179)
    )
    saturation_lower = fields.Integer(
        required=True,
        validate=validate.Range(min=0, max=255)
    )
    value_lower = fields.Integer(
        required=True,
        validate=validate.Range(min=0, max=255)
    )
    hue_upper = fields.Integer(
        required=True,
        validate=validate.Range(min=0, max=179)
    )
    saturation_upper = fields.Integer(
        required=True,
        validate=validate.Range(min=0, max=255)
    )
    value_upper = fields.Integer(
        required=True,
        validate=validate.Range(min=0, max=255)
    )


    @pre_load()
    def process_fields(self, data, **kwargs):
        self.user_id = get_jwt_identity()
        required_fields = [
            'image_name',
            'hue_lower', 'saturation_lower', 'value_lower',
            'hue_upper', 'saturation_upper', 'value_upper',
            'mask_type'
        ]

        for field in required_fields:
            if field not in data:
                raise ValidationError(f"Missing required field: {field}")

        return data


class RgbDBValidator:

    @staticmethod
    def validate_image_name(user_id, image_name):
        image_document = FilesModel.get_file_by_type_name_user(user_id, image_name, 'rgb')
        if not image_document:
            raise ValidationError(f"image {image_name} not found, please upload first!")
        return image_document

