from flask.views import MethodView, request
from flask_smorest import Blueprint


from validators.uploads import FileSchema, FileUploadSchema

from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
)

from swagger.uploads import (
    uploaded_successfully,
    retrieved_successfully,
)

from common import file_uploads
from common.http_status_codes import HTTP_200_OK


from models.files import FilesModel

blp = Blueprint("uploads", "uploads", description="File Uploads")


@blp.route("/uploads")
class Uploads(MethodView):

    @jwt_required()
    @blp.arguments(FileSchema, location="query")
    @blp.response(**retrieved_successfully)
    def get(self, data):
        print(data)
        user_id = get_jwt_identity()
        file_type = data.get("file_type", "")
        file_extension = data.get("file_extension", "")
        file_name = data.get("file_name", "")
        uploadedFiles = FilesModel.files_list_user(
            user_id, file_type, file_extension, file_name
        )
        processed_files = []
        for file in uploadedFiles:
            file["file_path"] = file_uploads.get_full_path(file["file_path"])
            processed_files.append(file)

        return processed_files

    @jwt_required()
    @blp.arguments(FileUploadSchema)
    @blp.response(**uploaded_successfully)
    def post(self, data):
        files = data["files"]
        for file in files:
            print(file)
            file["fileObject"].save(file["file_path"])
            del file["fileObject"]
        FilesModel.create_files(files)

        return {"message": "Files uploaded successfully."}, HTTP_200_OK
