from pymongo import MongoClient
import os


client = MongoClient(
    host=os.getenv("MONGO_DB_HOST", "localhost"),
    port=int(os.getenv("MONGO_DB_PORT", 27017)),
    username=os.getenv("MONGO_INITDB_ROOT_USERNAME", "root"),
    password=os.getenv("MONGO_INITDB_ROOT_PASSWORD", "pass"),
    maxPoolSize=os.getenv("MONGO_MAX_POOL_SIZE", 50),
    authSource=os.environ.get("DATABASE_AUTH_SOURCE"),
)

db = client[os.getenv("MONGO_INITDB_DATABASE", "analysis_data")]
