from pymongo import ASCENDING, DESCENDING

from db import db
from passlib.hash import pbkdf2_sha256
from datetime import datetime

from utility import to_ObjectId


class UploadsDB:
    collection = db["uploads"]