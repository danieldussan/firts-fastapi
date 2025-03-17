import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_TIME = int(os.getenv("ACCESS_TOKEN_EXPIRE_HOURS", "60"))
MONGODB_URI = os.getenv("MONGODB_URI")
