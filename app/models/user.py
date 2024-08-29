from pymongo import ASCENDING, DESCENDING
from pymongo.errors import DuplicateKeyError


from db import db
from passlib.hash import pbkdf2_sha256
from datetime import datetime

from utility import to_ObjectId


class UserDB:
    collection = db["users"]


class UserModel(UserDB):

    @classmethod
    def users_count(cls):
        return cls.collection.count_documents({"is_admin": False})

    @classmethod
    def users_list(cls):
        return cls.collection.find(
            {"is_admin": False}, {"password": 0, "is_admin": 0}
        ).sort("created_at", DESCENDING)

    @classmethod
    def create_user(cls, email, password, code=None, is_admin=False, **extra_data):
        """
        Create a new user.
        """
        current_utc_time = datetime.utcnow()
        user = {
            "email": email,
            "password": pbkdf2_sha256.hash(password),
            "is_admin": is_admin,
            **extra_data,
            "created_at": current_utc_time,
            "updated_at": current_utc_time,
        }
        if code:
            user.update({"code": code})
        return cls.collection.insert_one(user)

    @classmethod
    def create_default_admin(cls, email=None, password=None, **extra_data):
        try:
            cls.create_user(
                email=email or "admin@admin.com",
                password=password or "123456789",
                is_admin=True,
                **extra_data
            )
        except DuplicateKeyError:
            pass
        except Exception as e:
            print(e)

    @classmethod
    def update_user(cls, user_id, data: dict):
        current_utc_time = datetime.utcnow()
        if data.get("password"):
            data["password"] = pbkdf2_sha256.hash(data["password"])
        data["updated_at"] = current_utc_time
        return cls.collection.find_one_and_update(
            {"_id": to_ObjectId(user_id)}, {"$set": data}
        )

    @classmethod
    def delete_user(cls, user_id):
        cls.collection.delete_one({"_id": to_ObjectId(user_id)})

    @classmethod
    def get_user_by_email(cls, email):
        return cls.collection.find_one({"email": email})

    @classmethod
    def get_user_by_id(cls, id):
        if isinstance(id, str):
            id = to_ObjectId(id)
        return cls.collection.find_one({"_id": id})


class UserDBManager(UserDB):
    @classmethod
    def create_email_index(cls):
        """
        Create a unique index on the email field to ensure no duplicate emails.
        """
        cls.collection.create_index("email", unique=True)
