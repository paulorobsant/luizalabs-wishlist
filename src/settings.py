import os

from dotenv import load_dotenv
from starlette.datastructures import CommaSeparatedStrings

load_dotenv('.env')

"""
    General
"""

PROJECT_NAME = os.getenv("PROJECT_NAME", "be")
SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
SERVER_PORT = int(os.getenv("SERVER_PORT", 8001))
ENV_NAME = os.getenv("ENV", "local")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3001")
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
PSQL_DB = os.getenv("PSQL_DB", "be")

PSQL_URL = f"postgres://{PSQL_USER}:{PSQL_PASS}@{PSQL_HOST}:{PSQL_PORT}/{PSQL_DB}"

"""
    Mongo DB
"""

MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_PORT = int(os.getenv("MONGO_PORT", "27017"))
MONGO_URL = f"mongodb://{MONGO_HOST}:{MONGO_PORT}/"

"""
    RabbitMQ
"""

RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS", "guest")
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBIT_URL = f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@{RABBITMQ_HOST}//"

"""
    Security
"""

SECRET_KEY = "Drmhze6EPcv0fN_81Bj-nA"
ALGORITHM = "HS256"

"""
    Session
"""

JWT_TOKEN_PREFIX = "Token"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7

"""
    Email
"""

SMTP_TLS: bool = os.getenv("SMTP_TLS", "true") == "true"
SMTP_PORT = os.getenv("SMTP_PORT", "")
SMTP_HOST = os.getenv("SMTP_HOST", "localhost")
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
EMAILS_FROM_EMAIL = 'helena@globaltouch.tech'
EMAILS_FROM_NAME = 'Helena da Global Touch'
EMAILS_ENABLED = os.getenv("EMAILS_ENABLED", True)
EMAIL_TEMPLATES_DIR = f"{BASE_PATH}/templates"
EMAIL_RESET_TOKEN_EXPIRE_HOURS = 48

"""
    Social Authentication
"""

LINKEDIN_URL = "http://www.linkedin.com/oauth/v2/accessToken"
LINKEDIN_EMAIL_URL = "https://api.linkedin.com/v2/emailAddress?q=members&projection=(elements*(handle~))"
LINKEDIN_ME_URL = "https://api.linkedin.com/v2/me"
LINKEDIN_CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID", "")
LINKEDIN_SECRET_KEY = os.getenv("LINKEDIN_SECRET_KEY", "")

"""
    Machine Learning
"""

MODEL_DIR = f"{BASE_PATH}/match/classification/"

"""
    Queues
"""

QUEUE_RECOMMENDATIONS = f"queue_recommendations"
QUEUE_EMAILS = f"queue_emails"
QUEUE_OVERFLOWED_CONNECTIONS = f"queue_overflowed_connections"

"""
    Celery Routes
"""

TASK_RECOMMENDATION_FIND_CONNECTION = "recommendation.tasks.find_connection"
TASK_RECOMMENDATION_FIND_CONNECTION_FOR_OVERFLOWED = "recommendation.tasks.find_connection_overflowed"
TASK_ALERT_CONNECTION = "recommendation.tasks.alert_connection"

"""
    Celery Schedule
"""

SCHEDULE_RECOMMENDATION_FIND_CONNECTION = float(os.getenv("SCHEDULE_RECOMMENDATION_FIND_CONNECTION", 10))
SCHEDULE_TASK_ALERT_CONNECTION = float(os.getenv("SCHEDULE_TASK_ALERT_CONNECTION", 10))

"""
    Recommendations Settings
"""

MAX_NUMBER_ITERATIONS_FIND_CONNECTION = 10
