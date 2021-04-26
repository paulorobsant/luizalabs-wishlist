from typing import Generator

from core.database.session import Session


def get_db() -> Generator:
    """
    Returns a single database connection
    :return:
    """
    db = None

    try:
        db = Session()
        yield db
    finally:
        db.close()
