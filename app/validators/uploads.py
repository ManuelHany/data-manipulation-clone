from marshmallow import Schema, fields, validates, ValidationError, post_load, pre_load

from common.custom_fields import ObjectIdField
from constants import (
    EMAIL_ALREADY_EXISTS_KEY,
    USER_NOT_EXISTS_KEY,
    CODE_ALREADY_EXISTS_KEY,
)
from models.uploads import UploadsModel

from common.file_types import (
    PICTURE_EXTENSIONS,
    TABULAR_DATA_EXTENSIONS,
    TEXTUAL_DATA_EXTENSIONS
)

class UploadSchema(Schema):

    @pre_load
    def check_extension(self, payload):
        print("heeeeeeeeeeeeere")
        print(payload)