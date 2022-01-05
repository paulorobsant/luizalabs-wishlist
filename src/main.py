import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

import settings
from router import router

if __name__ == "__main__":

    """
        Env. Variables
    """

    load_dotenv('.env')

    """
        General
    """

    app = FastAPI(title=settings.PROJECT_NAME)

    if not settings.ALLOWED_HOSTS:
        ALLOWED_HOSTS = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    """
        Server
    """
    app.include_router(router, prefix=settings.API_STR)

    uvicorn.run(app, host=settings.SERVER_HOST, port=settings.SERVER_PORT)
