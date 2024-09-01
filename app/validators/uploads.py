from marshmallow import Schema, fields, validates, ValidationError, post_load, pre_load
import os
from flask import request
from flask_jwt_extended import get_jwt_identity


from models.files import FilesModel

from common.file_types import (
    PICTURE_EXTENSIONS,
    TABULAR_DATA_EXTENSIONS,
    TEXTUAL_DATA_EXTENSIONS
)

class FileSchema(Schema):
    file_path = fields.String()
    file_type = fields.String()
    file_extension = fields.String()
    file_name = fields.String()


class FileUploadSchema(Schema):
    files = fields.List(fields.Raw(required=True), required=True)

    @pre_load
    def process_files(self, data, **kwargs):
        """Extracts and validates the files from the incoming request."""
        if 'files' not in request.files:
            raise ValidationError('No files part in the request.')
        files = request.files.getlist('files')

        if not files:
            raise ValidationError('No selected files.')

        for file in files:
            FileDBValidator.validate_file_type(file)
        data['files'] = files
        return data

    @post_load
    def make_validated_files(self, data, **kwargs):
        """Transforms raw file data into validated file information."""
        files = data['files']
        validated_files = []
        for fileStorageObject in files:
            filename_with_extension = fileStorageObject.filename
            file_name, extension = os.path.splitext(filename_with_extension)
            extension = extension.strip(".")
            user_id = get_jwt_identity()

            if extension in TABULAR_DATA_EXTENSIONS:
                file_type = "tabular"
                file_path = os.path.join(os.getenv('TABULAR_FILESTORAGE', '/media/tabular'), filename_with_extension)
            elif extension in TEXTUAL_DATA_EXTENSIONS:
                file_type = "textual"
                file_path = os.path.join(os.getenv('TEXTUAL_FILESTORAGE', '/media/textual'), filename_with_extension)
            elif extension in PICTURE_EXTENSIONS:
                file_type = "rgb"
                file_path = os.path.join(os.getenv('RGB_FILESTORAGE', '/media/rgb'), filename_with_extension)
            else:
                raise Exception("file extension validator error.")

            if FilesModel.get_file_by_name_user(user_id, file_name):
                raise ValidationError(f"{filename_with_extension} file already exists, please remove it from uploads.")

            validated_files.append({
                "fileObject": fileStorageObject,
                "user_id": user_id,
                "file_type": file_type,
                "file_extension": extension,
                "file_name": file_name,
                "file_path": file_path,
            })
        return {'files': validated_files}


class FileDBValidator:
    @staticmethod
    def validate_file_type(file):
        if '.' not in file.filename:
            raise ValidationError('File must have an extension.')
        extension = file.filename.rsplit('.')[-1].lower()
        if extension not in PICTURE_EXTENSIONS + TABULAR_DATA_EXTENSIONS + TEXTUAL_DATA_EXTENSIONS:
            raise ValidationError(f'File type {extension} is not allowed.')
        return extension
