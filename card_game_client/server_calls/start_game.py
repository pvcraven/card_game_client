# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import json
import requests

def start_game(server, game_code):
    payload = {'game_code': game_code}
    response = requests.post(f"{server}/start_game/", json=payload)

    create_game_object = json.loads(response.text)
    return create_game_object
