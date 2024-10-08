from flask import Flask, jsonify, send_from_directory
from flask_smorest import Api
from flask_jwt_extended import JWTManager


from blocklist import BLOCKLIST
from models.user import UserDBManager, UserModel
from resources.users import blp as UserBlueprint
from resources.uploads import blp as UploadsBlueprint
from resources.rgb import blp as RgbBlueprint


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")
    set_db_indexes(app)
    UserModel.create_default_admin()
    jwt = JWTManager(app)

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {
                    "description": "The token is not fresh.",
                    "error": "fresh_token_required",
                }
            ),
            401,
        )

    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        try:
            user = UserModel.get_user_by_id(identity)
            return {"is_admin": user["is_admin"]}
        except Exception as e:

            return {
                "is_admin": False,
                "exception": e
            }

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {
                    "message": "The token has expired.",
                    "error": "token_expired",
                }
            ),
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {
                    "message": "Signature verification failed.",
                    "error": "invalid_token",
                }
            ),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token.",
                    "error": "authorization_required",
                }
            ),
            401,
        )

    api = Api(app)
    api.register_blueprint(UserBlueprint)
    api.register_blueprint(UploadsBlueprint)
    api.register_blueprint(RgbBlueprint)
    return app


def set_db_indexes(app):
    with app.app_context():
        UserDBManager.create_email_index()


app = create_app()


@app.get('/media/<path:path>')
def send_media(path):
    """
    Serve files from the media directory.

    :param path: a path like "posts/<int:post_id>/<filename>"
    :return: The file requested from the media directory
    """
    # Define the media directory
    media_directory = "/app/media"
    # Serve the file from the media directory
    return send_from_directory(directory=media_directory, path=path, as_attachment=True)
