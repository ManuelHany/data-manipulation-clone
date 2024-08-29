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
        files = []
        for fileStorageObject in data['files']:
            filename = fileStorageObject.filename
            name, extension = os.path.splitext(filename)
            extension = extension.strip(".")
            file_type = ""
            if extension in TABULAR_DATA_EXTENSIONS:
                file_type = "tabular"
                file_path = os.path.join(os.getenv('TABULAR_FILESTORAGE', '/media/tabular'), filename)
            elif extension in TEXTUAL_DATA_EXTENSIONS:
                file_type = "textual"
                file_path = os.path.join(os.getenv('RGB_FILESTORAGE', '/media/rgb'), filename)
            elif extension in PICTURE_EXTENSIONS:
                file_type = "rgb"
                file_path = os.path.join(os.getenv('TEXTUAL_FILESTORAGE', '/media/textual'), filename)
            else:
                raise Exception ("file extension validator error.")
            files.append({
                "user_id": get_jwt_identity(),
                "file_type": file_type,
                "file_extension": extension,
                "file_name": name,
                "file_path": file_path,
            })
            fileStorageObject.save(file_path)
        FilesModel.create_files(files)
        return('zangar')
