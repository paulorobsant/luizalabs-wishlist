## Migrations

##### Run this extension to generate uuid
```
CREATE EXTENSION IF NOT EXISTS "uuid-ossp"
```

##### Create migration
```
alembic revision --autogenerate -m "MESSAGE"
```

##### Run migration
```
alembic upgrade head
```

## Run Automatic Tasks

##### Run worker
```
celery -A worker --beat --app=tasks --loglevel=info
```