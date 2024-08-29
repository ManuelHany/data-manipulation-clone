from marshmallow import Schema, fields, validates, ValidationError, post_load, pre_load
from flask import request

from common.custom_fields import ObjectIdField
from constants import (
    EMAIL_ALREADY_EXISTS_KEY,
    USER_NOT_EXISTS_KEY,
    CODE_ALREADY_EXISTS_KEY,
)
from models.files import FilesModel

from common.file_types import (
    PICTURE_EXTENSIONS,
    TABULAR_DATA_EXTENSIONS,
    TEXTUAL_DATA_EXTENSIONS
)

class FileSchema(Schema):
    user_id = fields.String(required=True)
    file_type = fields.String(required=True)
    file_extension = fields.String(required=True)
    file_name = fields.String(required=True)
    file_path = fields.String()
    upload_date = fields.Date()



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




class FileDBValidator:
    @staticmethod
    def validate_file_type(file):
        if '.' not in file.filename:
            raise ValidationError('File must have an extension.')
        extension = file.filename.rsplit('.')[-1].lower()
        if extension not in PICTURE_EXTENSIONS + TABULAR_DATA_EXTENSIONS + TEXTUAL_DATA_EXTENSIONS:
            raise ValidationError(f'File type {extension} is not allowed.')
        return extension
