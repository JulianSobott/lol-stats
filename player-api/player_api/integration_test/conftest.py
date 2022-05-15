from pytest import fixture
from sqlalchemy import create_engine
from fastapi_sqlalchemy import db

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
    with db():
        db.session.commit()
        yield
