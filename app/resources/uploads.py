from flask.views import MethodView, request
from flask_smorest import Blueprint, abort


from validators.uploads import FileSchema, FileUploadSchema

from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
)

from swagger.uploads import (
    uploaded_successfully,
    retrieved_successfully,
    refresh_token_failed_docs,
    refresh_token_docs,
    unauthorized_docs,
    success_docs
)

from common import file_uploads
from common.http_status_codes import HTTP_200_OK


from models import FilesModel
blp = Blueprint('uploads', 'uploads', description="File Uploads")


@blp.route("/uploads")
class Uploads(MethodView):

    @jwt_required()
    @blp.response(**retrieved_successfully)
    def get(self):
        user_id = get_jwt_identity()
        file_type = request.args.get('file_type', type=str)
        file_extension = request.args.get('file_extension', type=str)
        file_name = request.args.get('file_name', type=str)
        uploadedFiles = FilesModel.files_list_user(user_id, file_type, file_extension, file_name)
        processed_files = []
        for file in uploadedFiles:
            file['file_path'] = file_uploads.get_full_path(file['file_path'])
            processed_files.append(file)

        return processed_files

    @jwt_required()
    @blp.arguments(FileUploadSchema)
    @blp.response(**uploaded_successfully)
    def post(self, data):
        files = data['files']
        for file in files:
            print(file)
            file['fileObject'].save(file['file_path'])
            del file['fileObject']
        FilesModel.create_files(files)

        return {'message': 'Files uploaded successfully.'}, HTTP_200_OK
