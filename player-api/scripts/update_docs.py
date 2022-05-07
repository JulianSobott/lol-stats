import yaml
from pathlib import Path
from fastapi.testclient import TestClient

from player_api.main import app

client = TestClient(app)

response = client.get("/openapi.json")
spec = response.json()
with open(Path(__file__).parent.joinpath("../openapi.yaml"), "w") as f:
    yaml.dump(spec, f, sort_keys=False)
