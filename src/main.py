import sentry_sdk
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

import settings
from router import router
from seeds.input_companies import add_all_companies
from seeds.input_terms import add_all_terms
from seeds.input_users import add_all_users

"""
    Logs
"""

sentry_sdk.init(
    "https://f92f148c75904f54afa9589ad75e6dc2@o421890.ingest.sentry.io/5731692",
    traces_sample_rate=1.0,
    environment=settings.ENV_NAME
)

"""
    Env. Variables
"""

load_dotenv()

"""
    General
"""

app = FastAPI(title=settings.PROJECT_NAME)

if not settings.ALLOWED_HOSTS:
    ALLOWED_HOSTS = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

"""
    Server
"""

app.include_router(router, prefix=settings.API_STR)

if __name__ == "__main__":
    add_all_terms()
    add_all_companies()

    if settings.ENV_NAME == 'local':
        add_all_users(n=20)

    uvicorn.run(app, host=settings.SERVER_HOST, port=settings.SERVER_PORT)
