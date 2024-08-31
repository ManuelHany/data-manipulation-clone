from flask import redirect, url_for, jsonify, send_file
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from marshmallow import ValidationError


from validators.rgb import MaskGenerationSchema, ImageSchema, FormatImageSchema

from flask_jwt_extended import (
    get_jwt_identity,
    get_jwt,
    jwt_required,
)

from swagger.uploads import (
    refresh_token_failed_docs,
    refresh_token_docs,
    unauthorized_docs,
    success_docs
)
from common.file_types import (
    TEXTUAL_DATA_EXTENSIONS,
    TABULAR_DATA_EXTENSIONS,
    PICTURE_EXTENSIONS
)
from common.rgb import (
    generate_segmentation_mask,
    generate_color_histogram,
    format_image,
    crop,
    resize
)
from common.http_status_codes import (
    HTTP_201_CREATED,
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_204_NO_CONTENT,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN
)


from models import FilesModel
blp = Blueprint('rgb', 'rgb', description="Operations on RGB images")


@blp.route("/rgb")
class Rgb(MethodView):

    @jwt_required()
    def get(self):
        file_type = 'rgb'
        return redirect(url_for('uploads.Uploads', file_type=file_type))

@blp.route("/rgb/format")
class FormatImage(MethodView):

    @jwt_required()
    @blp.arguments(FormatImageSchema, location='query')
    def get(self, validated_data):
        image_path = validated_data['image_path']
        output_format = validated_data['output_format']
        result = format_image(image_path, output_format)
        return result


@blp.route("/rgb/histogram-generation")
class HistogramGeneration(MethodView):

    @jwt_required()
    @blp.arguments(ImageSchema, location='query')
    def get(self, validated_data):
        result = generate_color_histogram(validated_data['image_path'])
        return result


@blp.route("/rgb/mask-generation")
class MaskGeneration(MethodView):

    @jwt_required()
    @blp.arguments(MaskGenerationSchema, location='query')
    def get(self, validated_data):
        lower_bound=[
            validated_data['hue_lower'],
            validated_data['saturation_lower'],
            validated_data['value_lower']
        ]
        upper_bound = [
            validated_data['hue_upper'],
            validated_data['saturation_upper'],
            validated_data['value_upper']
        ]
        result = generate_segmentation_mask(
            validated_data['image_path'],
            lower_bound,
            upper_bound,
            validated_data['mask_type']
        )

        # Return JSON response with mask
        return result
