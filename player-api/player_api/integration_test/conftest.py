from pytest import fixture

from db import Base, engine
from main import get_db


@fixture
def db_session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield from get_db()
