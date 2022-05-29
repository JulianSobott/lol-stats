import random
import string
import time

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from player_api.db import SessionLocal
from player_api.log import get_logger

logger = get_logger(__name__)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class LogRequestsMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        rid = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
        logger.info(f"{rid=} path={request.url.path}")
        start_time = time.time()

        response = await call_next(request)

        process_time = (time.time() - start_time) * 1000
        formatted_process_time = "{0:.2f}".format(process_time)
        logger.info(
            f"{rid=} completed_in={formatted_process_time}ms status_code={response.status_code}"
        )

        return response
