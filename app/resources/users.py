from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from marshmallow import ValidationError
from validators.users import (
    UserSchema,
    CreateUserSchema,
    GetUserByEmailSchema,
    GetUserByIdSchema,
    UpdateUserSchema,
    UserDBValidator
)

from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    get_jwt,
    jwt_required,
)
from swagger.admin import (
    success_docs,
    unauthorized_docs,
    invalid_token_docs,
    missing_token_docs,
    get_user_docs,
    update_user_docs,
    delete_user_docs,
    user_list_sample,
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

from models import UserModel
from blocklist import BLOCKLIST

blp = Blueprint('users', 'users', description="Operations on users")

@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "Successfully logged out"}, HTTP_200_OK


@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(CreateUserSchema)
    @blp.response(**success_docs)
    def post(selfself, user_data):
        if UserModel.get_user_by_email(user_data["email"]):
            abort(409, message="A user with this email already exists.")

        created_id = UserModel.create_user(**user_data, is_admin=False).inserted_id
        return {
                   "message": "User created successfully",
                   "user_id": str(created_id),
                   "user_email": user_data["email"],
               }, HTTP_201_CREATED


@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    @blp.response(**success_docs)
    @blp.alt_response(**unauthorized_docs)
    def post(self, user_data):
        user = UserModel.get_user_by_email(user_data["email"])
        if user and pbkdf2_sha256.verify(user_data["password"], user["password"]):
            access_token = create_access_token(str(user["_id"]), fresh=True)
            refresh_token = create_refresh_token(str(user["_id"]))
            return {"access_token": access_token, "refresh_token": refresh_token}, HTTP_200_OK

        abort(HTTP_401_UNAUTHORIZED, message="Invalid credentials.")

@blp.route("/user")
class User(MethodView):

    @jwt_required()
    @blp.arguments(GetUserByEmailSchema)
    @blp.response(HTTP_200_OK, GetUserByEmailSchema)
    def get(self, user_email):
        user = UserModel.get_user_by_email(user_email['email'])
        return user


@blp.route("/user/<string:user_id>")
class User(MethodView):

    @jwt_required()
    @blp.response(HTTP_200_OK, GetUserByIdSchema)
    def get(self, user_id):
        user = UserModel.get_user_by_id(user_id)
        return user

    @jwt_required(fresh=True)
    def delete(self, user_id):
        claims = get_jwt()
        if claims['is_admin']:
            user = UserModel.get_user_by_id(user_id)
            if user:
                UserModel.delete_user(user_id)
                return {"message": "User deleted."}, HTTP_200_OK
            else:
                return {"message": "User With this id not exists."}
        return {"message": "Action permitted for admins only."}, HTTP_403_FORBIDDEN




@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        # Make it clear that when to add the refresh token to the blocklist will depend on the app design
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"access_token": new_token}, HTTP_200_OK