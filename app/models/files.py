from pymongo import DESCENDING

from db import db
from datetime import datetime

from utility import to_ObjectId


class FilesDB:
    collection = db["files"]


class FilesModel(FilesDB):

    def files_count(cls, file_type="", file_extension=""):
        query = {}
        if file_type:
            query["file_type"] = file_type
        if file_extension:
            query["file_extension"] = file_extension
        return cls.collection.count_documents(query)

    @classmethod
    def files_list(cls, file_type="", file_extension="", file_name=""):
        query = {}
        if file_name:
            query["file_name"] = file_name
        if file_type:
            query["file_type"] = file_type
        if file_extension:
            query["file_extension"] = file_extension
        return cls.collection.find(query).sort("created_at", DESCENDING)

    @classmethod
    def files_count_user(cls, user_id, file_type="", file_extension=""):
        query = {"user_id": user_id}
        if file_type:
            query["file_type"] = file_type
        if file_extension:
            query["file_extension"] = file_extension
        return cls.collection.count_documents(query)

    @classmethod
    def files_list_user(cls, user_id, file_type="",
                        file_extension="", file_name=""):
        query = {"user_id": user_id}
        if file_name:
            query["file_name"] = file_name
        if file_type:
            query["file_type"] = file_type
        if file_extension:
            query["file_extension"] = file_extension

        # Projection to exclude _id and user_id
        projection = {"_id": 0, "user_id": 0}
        collection = cls.collection.find(query, projection)
        return collection.sort("created_at", DESCENDING)

    @classmethod
    def create_files(cls, docs):
        """
        Create a new files.
        """
        current_utc_time = datetime.utcnow()
        docs = [{**item, "upload_date": current_utc_time}for item in docs]
        return cls.collection.insert_many(docs)

    @classmethod
    def create_file(cls, user_id, file_type, file_extension,
                    file_name, file_path):
        """
        Create a new file.
        """
        current_utc_time = datetime.utcnow()
        file = {
            "user_id": user_id,
            "file_type": file_type,
            "file_extension": file_extension,
            "file_name": file_name,
            "file_path": file_path,
            "upload_date": current_utc_time,
        }
        return cls.collection.insert_one(file)

    @classmethod
    def delete_file(cls, file_id):
        cls.collection.delete_one({"_id": to_ObjectId(file_id)})

    @classmethod
    def get_files_by_name(cls, file_name):
        file = {"file_name": file_name}
        return cls.collection.find_many(file)

    @classmethod
    def get_file_by_name_user(cls, user_id, file_name):
        file = {"user_id": user_id, "file_name": file_name}
        return cls.collection.find_one(file)

    @classmethod
    def get_file_by_type_name_user(cls, user_id, file_name, file_type):
        file = {
            "user_id": user_id,
            "file_name": file_name,
            "file_type": file_type,
        }
        return cls.collection.find_one(file)

    @classmethod
    def get_file_by_id(cls, user_id, id):
        if isinstance(id, str):
            id = to_ObjectId(id)
        file = {user_id: user_id, "-id": id}
        return cls.collection.find_one({"_id": file})


class FilesDBManager(FilesDB):
    @classmethod
    def create_name_index(cls):
        """
        Create a unique index on the file_name
        field to ensure no duplicate emails.
        """
        cls.collection.create_index("file_name", unique=True)
