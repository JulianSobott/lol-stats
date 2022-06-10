from pytest import fixture

from player_api.db import Base, engine
from player_api.log import setup_logging
from player_api.middlewares import get_db

setup_logging()


@fixture
def db_session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield from get_db()
