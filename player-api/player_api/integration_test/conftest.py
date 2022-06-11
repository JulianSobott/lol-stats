from pytest import fixture

from player_api.db import Base, engine
from player_api.log import setup_logging
from player_api.middlewares import get_db
import player_api.middlewares

setup_logging()


@fixture
def db_session():
    player_api.middlewares.IS_TESTING = True
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield from get_db()
