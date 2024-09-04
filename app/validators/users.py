from marshmallow import (
    Schema,
    fields,
    validates,
    ValidationError,
    post_load,
    pre_load,
)

from constants import (
    EMAIL_ALREADY_EXISTS_KEY,
    USER_NOT_EXISTS_KEY,
)
from models.user import UserModel

from flask_jwt_extended import get_jwt_identity


class UserSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)
    is_admin = fields.Bool()
    created_at = fields.Date()


class CreateUserSchema(UserSchema):

    @validates("email")
    def validate_email(self, email):
        if UserModel.get_user_by_email(email):
            raise ValidationError("Email already exists.")

    @validates("password")
    def validate_password(self, value):
        if len(value) < 8:
            raise ValidationError("Password must be "
                                  "at least 8 characters long.")


class GetUserByEmailSchema(Schema):
    email = fields.Email(required=True)

    @pre_load()
    def check_is_admin(self, data, **kwargs):
        UserDBValidator.check_is_admin(get_jwt_identity())
        return data

    @validates("email")
    def validate_email(self, email):
        user = UserModel.get_user_by_email(email)
        if not user:
            raise ValidationError("User With this email not exists.")
        self.context['user'] = user

    @post_load
    def add_user(self, data, **kwargs):
        data["user"] = self.context['user']
        return data


class GetUserByIdSchema(Schema):
    user_id = fields.Str(required=True)


    @pre_load()
    def check_is_admin(self, data, **kwargs):
        UserDBValidator.check_is_admin(get_jwt_identity())
        return data

    @validates("user_id")
    def validate_id(self, user_id):
        user = UserModel.get_user_by_id(user_id)
        if not user:
            raise ValidationError("User With this id not exists.")
        self.context['user'] = user

    @post_load
    def add_user(self, data, **kwargs):
        data["user"] = self.context['user']
        return data


class UpdateUserSchema(CreateUserSchema):
    @validates("email")
    def validate_email(self, email):
        pass

    @staticmethod
    def validate_user_in_database(data, user_id):
        user = UserDBValidator.user_id_exists(user_id)
        if user["email"] != data["email"]:
            UserDBValidator.user_email_already_exists(data["email"])


class UserDBValidator:
    @staticmethod
    def user_id_exists(user_id):
        user = UserModel.get_user_by_id(user_id)
        if user_id and not user:
            raise ValidationError(
                {USER_NOT_EXISTS_KEY: "User With this id not exists."}
            )
        return user

    @staticmethod
    def user_email_already_exists(email):
        user = UserModel.get_user_by_email(email)
        if user:
            raise ValidationError(
                {EMAIL_ALREADY_EXISTS_KEY: "Email already in use."}
            )

    @staticmethod
    def check_is_admin(client_id):
        client_id = get_jwt_identity()
        if not UserModel.get_user_by_id(client_id)["is_admin"]:
            raise ValidationError("you are not authorized "
                                  "to perform this action.")
        return True
