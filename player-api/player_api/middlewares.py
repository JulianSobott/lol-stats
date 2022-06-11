import os
import random
import string
import time

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from player_api.db import (
    SessionLocal,
    AsyncSessionLocal,
    db_user,
    db_pw,
    db_host,
    db_port,
    db_database,
    db_type,
)
from player_api.log import get_logger

logger = get_logger(__name__)

IS_TESTING = False


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_async_db():
    if IS_TESTING:
        async_engine = create_async_engine(
            f"{db_type}+asyncpg://{db_user}:{db_pw}@{db_host}:{db_port}/{db_database}",
        )
        session = sessionmaker(
            autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession
        )
        async with session() as db:
            try:
                yield db
            finally:
                async_engine.sync_engine.dispose()
    else:
        async with AsyncSessionLocal() as db:
            yield db


class LogRequestsMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        rid = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
        logger.info(f"{rid=} path={request.url}")
        start_time = time.time()

        response = await call_next(request)

        process_time = (time.time() - start_time) * 1000
        formatted_process_time = "{0:.2f}".format(process_time)
        logger.info(
            f"{rid=} completed_in={formatted_process_time}ms status_code={response.status_code}"
        )

        return response
