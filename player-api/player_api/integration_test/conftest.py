from pytest import fixture
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from db import Base
from integration_test.test_main import Champion


@fixture
def db_session():
    engine = create_engine(
        f"postgresql://postgres:postgres@localhost/postgres",
    )
    Champion.cache = {}
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    session = Session()
    yield session
    session.close()
