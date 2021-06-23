import os
import sys
from logging.config import fileConfig
from typing import List

from sqlalchemy import engine_from_config, MetaData
from sqlalchemy import pool
from alembic import context

parent_dir = os.path.abspath(os.getcwd())
sys.path.append(parent_dir)

from core.database.session import Base
from settings import PSQL_URL

db_url = PSQL_URL.replace("%", "%%")

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
config.set_main_option("sqlalchemy.url", db_url)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here

from models import *

target_metadata = Base.metadata
schemas = ["public", "logs"]


def _include_object(target_schema):
    def include_object(obj, name, object_type, reflected, compare_to):
        if object_type == "table":
            return obj.schema in target_schema
        else:
            return True

    return include_object


def _run_migrations_offline(target_metadata, schema):
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = PSQL_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_schemas=True,  # 1
        include_object=_include_object(schema),  # 1
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def _run_migrations_online(target_metadata, schema):
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        url=PSQL_URL,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_schemas=True,  # 2
            include_object=_include_object(schema),  # 2
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


def run_migrations(metadata: MetaData, schemas: List[str]):
    if context.is_offline_mode():
        _run_migrations_offline(metadata, schemas)
    else:
        _run_migrations_online(metadata, schemas)


run_migrations(metadata=target_metadata, schemas=schemas)
