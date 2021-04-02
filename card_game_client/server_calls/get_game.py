import json
import requests


def get_game(server, game_code):
    payload = {'game_code': game_code}
    response = requests.get(f"{server}/get_game/", json=payload)

    create_game_object = json.loads(response.text)
    return create_game_object
