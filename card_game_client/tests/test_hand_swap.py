from server_calls.create_game import create_game
from server_calls.join_game import join_game
from server_calls.list_games import list_games
from server_calls.get_game import get_game
from server_calls.start_game import start_game
from server_calls.move_to_hold import move_to_hold
from server_calls.move_to_pile import move_to_pile
from server_calls.add_computer_player import add_computer_player
from print_hand import print_hand
from game_ui_text import display_all

server = "http://127.0.0.1:8000"
names = 'Mary', 'Sam', 'Bob', 'Jane'

MODE_LOBBY = 'Lobby'
MODE_PICK_FROM_HAND = 'Pick from hand'
MODE_PICK_FROM_HOLD = 'Pick from hold'


def test_stuff():

    name = 'Mary'

    # Create a game
    result = create_game(server, names[0])
    assert result
    assert 'game_code' in result
    game_code = result['game_code']

    # Get a list of the games
    result = list_games(server)
    assert result
    assert game_code in result
    game = result[game_code]
    assert 'user_list' in game
    user_list = game['user_list']
    assert len(user_list) == 1
    assert 'Mary' in user_list

    # Get a single game
    result = get_game(server, game_code)
    assert 'user_list' in result
    assert name in user_list

    game = add_computer_player(server, game_code)
    game = start_game(server, game_code)

    for i in range(2):
        hand = game['user_list'][name]['hand']['card_list']
        draw = hand[0]
        draw_number = draw['number']
        print(f"Move to hold {draw_number}")
        game = move_to_hold(server, game_code, name, draw_number)

    hand2 = game['user_list'][name]['hand']
    print()
    print(hand2)

    # display_all(game, name)

    for i in range(2):
        hold = game['user_list'][name]['hold']['card_list']
        draw = hold[0]
        draw_number = draw['number']
        game = move_to_pile(server, game_code, name, draw_number, 1)

    hand3 = game['user_list'][name]['hand']
    print()
    print(hand3)
    assert hand2 != hand3

    # display_all(game, name)
