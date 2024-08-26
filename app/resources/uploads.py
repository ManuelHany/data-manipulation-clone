from flask.views import MethodView
from flask_smorest import Blueprint, abort
from validators.uploads import UploadSchema

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
from common.http_status_codes import (
    HTTP_201_CREATED,
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_204_NO_CONTENT,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN
)

from models.uploads import UploadsDB
blp = Blueprint('uploads', 'uploads', description="Operations on RGB images")


@blp.route("/uploads")
class Uploads(MethodView):
    print("zangar")

    @jwt_required()
    def post(self, payload):
        print("hereeeeeeeeeeeeeeeeeee")
        return payload
