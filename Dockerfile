FROM python:3.7

WORKDIR app
COPY /src /app
COPY /environments/.env.production /app/.env
COPY requirements.txt /app/requirements.txt

RUN pip install -r ./requirements.txt

EXPOSE 80
CMD ["main.py"]
ENTRYPOINT ["python3"]

