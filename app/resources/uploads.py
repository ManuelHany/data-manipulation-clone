from flask.views import MethodView
from flask_smorest import Blueprint, abort

import os
from werkzeug.datastructures import FileStorage

from validators.uploads import FileUploadSchema

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
blp = Blueprint('uploads', 'uploads', description="Operations on RGB images")


@blp.route("/uploads")
class Uploads(MethodView):

    @jwt_required()
    @blp.arguments(FileUploadSchema)
    def post(self, data):
        files = data['files']
        for file in files:
            file['fileObject'].save(file['file_path'])
            del file['fileObject']
        FilesModel.create_files(files)

        return {'message': 'Files uploaded successfully.'}, HTTP_200_OK
