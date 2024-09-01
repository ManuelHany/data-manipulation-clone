from marshmallow import (
    Schema,
    fields,
    validate,
    validates,
    ValidationError,
    post_load,
    pre_load,
)
from flask_jwt_extended import get_jwt_identity

from common.rgb import get_width_height
from common.file_types import PICTURE_EXTENSIONS

from models.files import FilesModel


class ImageSchema(Schema):
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
        image_document = RgbDBValidator.validate_image_name(
            user_id, image_name
        )
        self.image_path = image_document["file_path"]

    @post_load
    def include_additional_fields(self, data, **kwargs):
        data["user_id"] = self.user_id
        data["image_path"] = self.image_path
        return data


class CropSchema(ImageSchema):
    x = fields.Integer(
        required=True, validate=validate.Range(min=0))
    y = fields.Integer(
        required=True, validate=validate.Range(min=0))
    width = fields.Integer(
        required=True, validate=validate.Range(min=0))
    height = fields.Integer(
        required=True, validate=validate.Range(min=0))

    @post_load
    def include_additional_fields(self, data, **kwargs):
        data["user_id"] = self.user_id
        data["image_path"] = self.image_path
        x = data["x"]
        y = data["y"]
        width = data["width"]
        height = data["height"]
        RgbDBValidator.validate_image_dimensions(
            data["image_path"], [x, width], [y, height]
        )
        return data


class ResizeSchema(ImageSchema):
    width = fields.Integer(
        required=True,
        validate=validate.Range(min=10, max=4096))
    height = fields.Integer(
        required=True,
        validate=validate.Range(min=10, max=4096))

    @post_load()
    def validate_aspect_ratio(self, data, **kwargs):
        width = data["width"]
        height = data["height"]
        RgbDBValidator.validate_aspect_ratio(width, height)
        return data


class FormatImageSchema(ImageSchema):
    output_format = fields.Str(
        required=True, validate=validate.OneOf(PICTURE_EXTENSIONS)
    )


class MaskGenerationSchema(ImageSchema):
    mask_type = fields.Str(
        required=True,
        validate=validate.OneOf(
            ["bitwise_and", "bitwise_or", "bitwise_xor", "bitwise_not"]),
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
        validate=validate.Range(min=0, max=255))

    @pre_load()
    def process_fields(self, data, **kwargs):
        self.user_id = get_jwt_identity()
        required_fields = [
            "image_name",
            "hue_lower",
            "saturation_lower",
            "value_lower",
            "hue_upper",
            "saturation_upper",
            "value_upper",
            "mask_type",
        ]

        for field in required_fields:
            if field not in data:
                raise ValidationError(f"Missing required field: {field}")

        return data


class RgbDBValidator:

    @staticmethod
    def validate_image_name(user_id, image_name):
        image_document = FilesModel.get_file_by_type_name_user(
            user_id, image_name, "rgb"
        )
        if not image_document:
            raise ValidationError(f"image {image_name} not "
                                  f"found, please upload first!")
        return image_document

    @staticmethod
    def validate_aspect_ratio(width, height):
        accepted_aspect_ratios = [(4, 3), (16, 9), (1, 1)]

        is_valid_aspect_ratio = False
        input_ratio = width / height
        for ratio in accepted_aspect_ratios:
            if input_ratio == ratio[0] / ratio[1]:
                is_valid_aspect_ratio = True
                break

        if not is_valid_aspect_ratio:
            raise ValidationError("Invalid aspect ratio. ")

    @staticmethod
    def validate_image_dimensions(image_path, width_list, height_list):
        img_width, img_height = get_width_height(image_path)

        for width in width_list:
            if width <= img_width:
                continue
            else:
                raise ValidationError("the width should be within image width")

        for height in height_list:
            if height <= img_height:
                continue
            else:
                raise ValidationError("the height should "
                                      "be within image height")
