FROM python:3.7

# This dockerfile is responsible for building the base image of the application as a whole.
# This image will be used by the central application and the celery application.

WORKDIR /app
COPY /src /app
COPY /environments/.env.production /app/.env
COPY /requirements.txt /app/requirements.txt
COPY /entrypoint.sh /app/entrypoint.sh

RUN pip install -r ./requirements.txt