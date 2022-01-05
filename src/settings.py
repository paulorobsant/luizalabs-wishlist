import os

from dotenv import load_dotenv
from starlette.datastructures import CommaSeparatedStrings

load_dotenv('.env')

"""
    General
"""

PROJECT_NAME = os.getenv("PROJECT_NAME", "LuizaLabs")
SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
SERVER_PORT = int(os.getenv("SERVER_PORT", 8001))
ENV_NAME = os.getenv("ENV", "local")
BASE_PATH = os.path.dirname(os.path.abspath(__file__))

"""
    API
"""

API_STR = "/api"
ALLOWED_HOSTS = CommaSeparatedStrings(os.getenv("ALLOWED_HOSTS", "*"))

"""
    Postgres DB
"""

PSQL_HOST = os.getenv("PSQL_HOST", "localhost")
PSQL_PORT = int(os.getenv("PSQL_PORT", "5432"))
PSQL_USER = os.getenv("PSQL_USER", "root")
PSQL_PASS = os.getenv("PSQL_PASS", "root")
PSQL_DB = os.getenv("PSQL_DB", "luizalabs")

PSQL_URL = f"postgres://{PSQL_USER}:{PSQL_PASS}@{PSQL_HOST}:{PSQL_PORT}/{PSQL_DB}"

"""
    Security
"""

SECRET_KEY = "7HghrAb6lP"
ALGORITHM = "HS256"

"""
    Session
"""

JWT_TOKEN_PREFIX = "Token"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7
