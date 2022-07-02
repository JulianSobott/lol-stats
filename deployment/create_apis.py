import os

import requests

base_url = "https://api-management.lol-stats.de/management/organizations/DEFAULT/environments/DEFAULT"
auth = ("admin", "admin")

for file in os.listdir("apis"):
    with open(f"apis/{file}", "r") as f:
        response = requests.post(f"{base_url}/apis/import", auth=auth, data=f.read())
    new_id = response.json()["id"]
    requests.post(f"{base_url}/apis/{new_id}/deploy", auth=auth, json={"deploymentLabel": "initial deployment"})
    requests.post(f"{base_url}/apis/{new_id}?action=START", auth=auth)
    print(f"API created and started: {file.replace('.json', '')}")
