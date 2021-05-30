import sentry_sdk
import rollbar
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

import settings
from router import router

if __name__ == "__main__":
    try:
        """
            Logs
        """

        sentry_sdk.init(
            "https://f92f148c75904f54afa9589ad75e6dc2@o421890.ingest.sentry.io/5731692",
            traces_sample_rate=1.0,
            environment=settings.ENV_NAME
        )

        rollbar.init("52839cbb5d2b478ca55d8766ce6b47f1", settings.ENV_NAME)

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
    except:
        rollbar.report_exc_info()
