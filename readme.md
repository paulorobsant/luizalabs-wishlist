## Get Started


##### Create a Postgres database using the credentials in environments folder.

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
