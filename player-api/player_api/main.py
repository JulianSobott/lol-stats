from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from player_api.log import setup_logging
from player_api.middlewares import LogRequestsMiddleware
from player_api.endpoints import import_player, find_player, get_player, recent_games


setup_logging()

app = FastAPI(
    title="Player API",
    version="1.0.0",
    servers=[{"url": "https://lol-stats.de/api"}],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(LogRequestsMiddleware)


app.include_router(get_player.router)
app.include_router(find_player.router)
app.include_router(import_player.router)
app.include_router(recent_games.router)


FastAPIInstrumentor.instrument_app(app)
