# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import json
import requests

def join_game(server, game_code, user_name):
    payload = {'user_name': user_name, 'game_code': game_code}
    response = requests.post(f"{server}/join_game/", json=payload)

    create_game_object = json.loads(response.text)
    return create_game_object
