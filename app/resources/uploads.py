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


from models.files import FilesDB
blp = Blueprint('uploads', 'uploads', description="Operations on RGB images")


@blp.route("/uploads")
class Uploads(MethodView):

    @jwt_required()
    @blp.arguments(FileUploadSchema)
    def post(self, data):
        for fileStorageObject in data['files']:
            filename = fileStorageObject.filename
            name, extension = os.path.splitext(filename)
            extension = extension.strip(".")
            if extension in TABULAR_DATA_EXTENSIONS:
                file_path = os.path.join(os.getenv('TABULAR_FILESTORAGE', '/media/tabular'), filename)
            elif extension in TEXTUAL_DATA_EXTENSIONS:
                file_path = os.path.join(os.getenv('RGB_FILESTORAGE', '/media/rgb'), filename)
            elif extension in PICTURE_EXTENSIONS:
                file_path = os.path.join(os.getenv('TEXTUAL_FILESTORAGE', '/media/textual'), filename)
            else:
                raise Exception ("file extension validator error.")
            # fileStorageObject.save(file_path)
            print(type(get_jwt_identity()))
        return('zangar')
