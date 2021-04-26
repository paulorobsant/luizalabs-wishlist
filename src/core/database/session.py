from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from settings import PSQL_URL, MONGO_HOST, MONGO_PORT
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

"""
    MongoDB
"""

client = MongoClient(host=MONGO_HOST, port=MONGO_PORT)