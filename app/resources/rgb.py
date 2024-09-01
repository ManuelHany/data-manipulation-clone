from flask import redirect, url_for
from flask.views import MethodView
from flask_smorest import Blueprint

from validators.rgb import (
    MaskGenerationSchema,
    ImageSchema,
    FormatImageSchema,
    ResizeSchema,
    CropSchema,
)

from flask_jwt_extended import (
    jwt_required,
)

from common.rgb import (
    generate_segmentation_mask,
    generate_color_histogram,
    format,
    crop,
    resize,
)


blp = Blueprint("rgb", "rgb", description="Operations on RGB images")


@blp.route("/rgb")
class Rgb(MethodView):

    @jwt_required()
    def get(self):
        file_type = "rgb"
        return redirect(url_for("uploads.Uploads", file_type=file_type))


@blp.route("/rgb/crop")
class CropImage(MethodView):

    @jwt_required()
    @blp.arguments(CropSchema, location="query")
    def get(self, validated_data):
        image_path = validated_data["image_path"]
        x = validated_data["x"]
        y = validated_data["y"]
        width = validated_data["width"]
        height = validated_data["height"]
        return crop(image_path, x, y, width, height)


@blp.route("/rgb/resize")
class ResizeImage(MethodView):

    @jwt_required()
    @blp.arguments(ResizeSchema, location="query")
    def get(self, validated_data):
        image_path = validated_data["image_path"]
        width = validated_data["width"]
        height = validated_data["height"]
        return resize(image_path, width, height)


@blp.route("/rgb/format")
class FormatImage(MethodView):

    @jwt_required()
    @blp.arguments(FormatImageSchema, location="query")
    def get(self, validated_data):
        image_path = validated_data["image_path"]
        output_format = validated_data["output_format"]
        return format(image_path, output_format)


@blp.route("/rgb/histogram-generation")
class HistogramGeneration(MethodView):

    @jwt_required()
    @blp.arguments(ImageSchema, location="query")
    def get(self, validated_data):
        result = generate_color_histogram(validated_data["image_path"])
        return result


@blp.route("/rgb/mask-generation")
class MaskGeneration(MethodView):

    @jwt_required()
    @blp.arguments(MaskGenerationSchema, location="query")
    def get(self, validated_data):
        lower_bound = [
            validated_data["hue_lower"],
            validated_data["saturation_lower"],
            validated_data["value_lower"],
        ]
        upper_bound = [
            validated_data["hue_upper"],
            validated_data["saturation_upper"],
            validated_data["value_upper"],
        ]
        result = generate_segmentation_mask(
            validated_data["image_path"],
            lower_bound,
            upper_bound,
            validated_data["mask_type"],
        )

        # Return JSON response with mask
        return result
