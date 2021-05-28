## Migrations

##### Run this extension to generate uuid
```
CREATE EXTENSION IF NOT EXISTS "uuid-ossp"
```

##### Create migration
```
$ alembic revision --autogenerate -m "MESSAGE"
```

##### Run migration
```
$ alembic upgrade head
```

## Run Automatic Tasks

```
$ celery -A periodic beat --loglevel=info
```

```
$ celery -A periodic worker --loglevel=info -E -Q {QUEUE_NAME}
```

## Run Mailhog

```
$ docker-compose up -d mailhog
```

## Run RabbitMQ

```
$ docker-compose up -d rabbit
```

## Run Docker

```
$ docker build -t global_touch/base -f ./deploy/Dockerfile .
```