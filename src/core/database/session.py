from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from settings import PSQL_URL
from pymongo import MongoClient

ENGINE = create_engine(
    PSQL_URL,
    encoding="utf-8",
    echo=True,
    pool_pre_ping=True
)

Session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=ENGINE
    )
)

Base = declarative_base()
Base.query = Session.query_property()