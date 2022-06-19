from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
import sentry_sdk
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

from player_api.middlewares import LogRequestsMiddleware
from player_api.endpoints import (
    import_player,
    find_player,
    get_player,
    recent_games,
    achievements,
    leaderboards,
)

sentry_sdk.init(
    dsn="https://2068deda898a4da48826ee7956fe3924@o1288571.ingest.sentry.io/6505584",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production,
    traces_sample_rate=1.0,
)

app = FastAPI(
    title="Player API",
    version="1.0.0",
    servers=[{"url": "https://lol-stats.de/api"}],
)

app.add_middleware(SentryAsgiMiddleware)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(LogRequestsMiddleware)
app.add_middleware(GZipMiddleware)


app.include_router(get_player.router)
app.include_router(find_player.router)
app.include_router(import_player.router)
app.include_router(recent_games.router)
app.include_router(achievements.router)
app.include_router(leaderboards.router)


FastAPIInstrumentor.instrument_app(app)
