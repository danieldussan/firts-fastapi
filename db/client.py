from pymongo import MongoClient
from const import MONGODB_URI

# Local
# db_client = MongoClient().local
#
# Remote
db_client = MongoClient(MONGODB_URI).users
