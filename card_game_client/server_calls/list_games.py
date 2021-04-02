import json
import requests


def list_games(server):
    response = requests.get(f"{server}/list_games/")

    result = json.loads(response.text)
    return result
