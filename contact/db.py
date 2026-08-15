import os
import sys
from pymongo import MongoClient
from pymongo.errors import PyMongoError

MONGO_URI = os.environ.get("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["portfolio_db"]
contact_messages_collection = db["contact_messages"]

try:
    client.admin.command("ping")
    print("MongoDB Atlas connection: OK")
except PyMongoError as e:
    print(f"WARNING: Could not connect to MongoDB Atlas at startup: {e}", file=sys.stderr)