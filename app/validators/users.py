from marshmallow import Schema, fields, validates, ValidationError, post_load

from common.custom_fields import ObjectIdField
from constants import (
    EMAIL_ALREADY_EXISTS_KEY,
    USER_NOT_EXISTS_KEY,
    CODE_ALREADY_EXISTS_KEY,
)
from models.user import UserModel



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
            raise ValidationError("Password must be at least 8 characters long.")


class GetUserByEmailSchema(UserSchema):
    _id = ObjectIdField()
    password = fields.Str(required=False, load_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    @validates("email")
    def validate_email(self, email):
        self.user = UserModel.get_user_by_email(email)
        if not self.user:
            raise ValidationError("User With this email not exists.")

    @post_load
    def add_user(self, in_data, **kwargs):
        in_data["user"] = self.user
        return in_data


class GetUserByIdSchema(UserSchema):
    _id = ObjectIdField(required=True)
    password = fields.Str(load_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    @validates("id")
    def validate_id(self, id):
        self.user = UserModel.get_user_by_id(id)
        if not self.user:
            raise ValidationError("User With this id not exists.")

    @post_load
    def add_user(self, in_data, **kwargs):
        in_data["user"] = self.user
        return in_data


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
                {EMAIL_ALREADY_EXISTS_KEY: "there is another user with this email."}
            )

