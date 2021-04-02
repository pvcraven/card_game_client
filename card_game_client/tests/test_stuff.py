from server_calls.create_game import create_game
from server_calls.join_game import join_game
from server_calls.list_games import list_games
from server_calls.get_game import get_game
from server_calls.start_game import start_game
from server_calls.move_to_hold import move_to_hold
from server_calls.move_to_pile import move_to_pile
from print_hand import print_hand

server = "http://127.0.0.1:8000"
names = 'Mary', 'Sam', 'Bob', 'Jane'

MODE_LOBBY = 'Lobby'
MODE_PICK_FROM_HAND = 'Pick from hand'
MODE_PICK_FROM_HOLD = 'Pick from hold'


def test_stuff():

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
    assert 'Mary' in user_list

    # Join a game person 2
    result = join_game(server, game_code, names[1])
    assert 'game_code' in result
    assert 'user_list' in result
    assert result['game_code'] == game_code

    # Get a list of the games
    result = list_games(server)
    assert result
    assert game_code in result
    game = result[game_code]
    assert 'user_list' in game
    user_list = game['user_list']
    assert len(user_list) == 2
    assert 'Mary' in user_list
    assert 'Sam' in user_list

    # Join a game that doesn't exist
    result = join_game(server, '00000', names[1])
    assert 'game_code' not in result
    assert 'user_list' not in result
    assert 'error' in result

    # Join a game person 3
    result = join_game(server, game_code, names[2])
    assert 'game_code' in result
    assert 'user_list' in result
    assert result['game_code'] == game_code

    # Join a game person 4
    result = join_game(server, game_code, names[3])
    assert 'game_code' in result
    assert 'user_list' in result
    assert result['game_code'] == game_code

    # Join a game person 5 (failed)
    result = join_game(server, game_code, 'Sally')
    assert 'game_code' not in result
    assert 'user_list' not in result
    assert 'error' in result

    # Start the game
    game = start_game(server, game_code)
    for name in names:
        hand = game['user_list'][name]['hand']['card_list']
        hold = game['user_list'][name]['hold']['card_list']
        pile1 = game['user_list'][name]['hold']['card_list']
        pile2 = game['user_list'][name]['pile2']['card_list']
        pile3 = game['user_list'][name]['pile3']['card_list']
        assert len(hand) == 10
        assert len(pile1) == 0
        assert len(pile2) == 0
        assert len(pile3) == 0
        assert len(hold) == 0

    # Get the game
    game = get_game(server, game_code)
    assert game['mode'] == MODE_PICK_FROM_HAND
    for name in names:
        hand = game['user_list'][name]['hand']['card_list']
        hold = game['user_list'][name]['hold']['card_list']
        pile1 = game['user_list'][name]['hold']['card_list']
        pile2 = game['user_list'][name]['pile2']['card_list']
        pile3 = game['user_list'][name]['pile3']['card_list']
        assert len(hand) == 10
        assert len(pile1) == 0
        assert len(pile2) == 0
        assert len(pile3) == 0
        assert len(hold) == 0

    print("ROUND 1")
    for name in names:
        for i in range(2):
            hand = game['user_list'][name]['hand']['card_list']
            draw = hand[0]['number']
            game = move_to_hold(server, game_code, name, draw)
            print_hand(game, name)

    assert game['mode'] == MODE_PICK_FROM_HOLD

    print("ROUND 1B")
    for name in names:
        for i in range(2):
            hold = game['user_list'][name]['hold']['card_list']
            draw = hold[0]['number']
            game = move_to_pile(server, game_code, name, draw, 1)
            print_hand(game, name)

    print("ROUND 2")
    for name in names:
        for i in range(2):
            hand = game['user_list'][name]['hand']['card_list']
            draw = hand[0]['number']
            game = move_to_hold(server, game_code, name, draw)
            print_hand(game, name)

    assert game['mode'] == MODE_PICK_FROM_HOLD


