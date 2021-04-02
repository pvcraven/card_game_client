# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import json
import requests

def move_to_hold(server, game_code, user_name, card):
    payload = {'user_name': user_name,
               'game_code': game_code,
               'card': card}
    response = requests.post(f"{server}/move_to_hold/", json=payload)
    create_game_object = json.loads(response.text)
    if 'error' in create_game_object:
        raise ValueError(f"Error moving {card} for {user_name}: {create_game_object['error']}")
    return create_game_object
