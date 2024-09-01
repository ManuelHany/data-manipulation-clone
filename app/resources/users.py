from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from validators.users import (
    UserSchema,
    CreateUserSchema,
    GetUserByEmailSchema,
    GetUserByIdSchema,
)

from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    get_jwt,
    jwt_required,
)
from swagger.user import (
    success_register_docs,
    success_docs,
    success_logout_docs,
    get_user_docs,
    unauthorized_docs,
    credentials_invalid_docs,
    refresh_token_docs,
    invalid_token_docs,
    missing_token_docs,
)
from utility import json_serializer
from common.http_status_codes import (
    HTTP_201_CREATED,
    HTTP_200_OK,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
)

from models.user import UserModel
from blocklist import BLOCKLIST

blp = Blueprint("users", "users", description="Operations on users")


@blp.route("/logout")
class UserLogout(MethodView):

    @jwt_required()
    @blp.response(**success_logout_docs)
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "Successfully logged out"}, HTTP_200_OK


@blp.route("/register")
class UserRegister(MethodView):

    @blp.arguments(CreateUserSchema)
    @blp.response(**success_register_docs)
    def post(selfself, user_data):
        if UserModel.get_user_by_email(user_data["email"]):
            abort(409, message="A user with this email already exists.")

        created_id = UserModel.create_user(
            **user_data, is_admin=False).inserted_id
        return {
            "message": "User created successfully",
            "user_id": str(created_id),
            "user_email": user_data["email"],
        }, HTTP_201_CREATED


@blp.route("/login")
class UserLogin(MethodView):

    @blp.arguments(UserSchema)
    @blp.response(**success_docs)
    @blp.alt_response(**credentials_invalid_docs)
    def post(self, user_data):
        user = UserModel.get_user_by_email(user_data["email"])
        if user and \
                pbkdf2_sha256.verify(user_data["password"], user["password"]):
            access_token = create_access_token(str(user["_id"]), fresh=True)
            refresh_token = create_refresh_token(str(user["_id"]))
            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
            }, HTTP_200_OK

        abort(HTTP_401_UNAUTHORIZED, message="Invalid credentials.")


@blp.route("/user")
class UserEmail(MethodView):

    @jwt_required()
    @blp.arguments(GetUserByEmailSchema)
    @blp.response(**get_user_docs)
    @blp.alt_response(**missing_token_docs)
    @blp.alt_response(**invalid_token_docs)
    @blp.alt_response(**unauthorized_docs)
    def get(self, data):
        user = data["user"]
        return {
            "_id": json_serializer(user["_id"]),
            "created_at": json_serializer(user["created_at"]),
            "email": user["email"],
            "is_admin": user["is_admin"],
        }, HTTP_200_OK


@blp.route("/user/<string:user_id>")
class UserID(MethodView):
    """Only Admins"""

    @jwt_required()
    @blp.arguments(GetUserByIdSchema, location="view_args")
    @blp.response(**get_user_docs)
    @blp.alt_response(**missing_token_docs)
    @blp.alt_response(**invalid_token_docs)
    @blp.alt_response(**unauthorized_docs)
    def get(self, data, user_id):
        print("here")
        user = data["user"]
        print(user)
        return {
            "_id": json_serializer(user["_id"]),
            "created_at": json_serializer(user["created_at"]),
            "email": user["email"],
            "is_admin": user["is_admin"],
        }, HTTP_200_OK

    @jwt_required(fresh=True)
    def delete(self, user_id):
        claims = get_jwt()
        if claims["is_admin"]:
            user = UserModel.get_user_by_id(user_id)
            if user:
                UserModel.delete_user(user_id)
                return {"message": "User deleted."}, HTTP_200_OK
            else:
                return {"message": "User With this id not exists."}
        return {
                   "message": "Action permitted for admins only."
               }, HTTP_403_FORBIDDEN


@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    @blp.response(**refresh_token_docs)
    @blp.alt_response(**missing_token_docs)
    @blp.alt_response(**invalid_token_docs)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        # Make it clear that when to add the refresh token
        # to the blocklist will depend on the app design
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"access_token": new_token}, HTTP_200_OK
