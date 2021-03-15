from server_calls.create_game import create_game
from server_calls.get_game import get_game
from server_calls.start_game import start_game
from server_calls.move_to_hold import move_to_hold
from server_calls.join_game import join_game
from server_calls.move_to_pile import move_to_pile
from server_calls.add_computer_player import add_computer_player

from constants import *

def get_card_by_id(card_pile, id):
    card_list = card_pile['card_list']
    for card in card_list:
        if card.number == id:
            return card
    return None

def get_choice(possible_choices):
    success = False
    while not success:
        choice = input("> ")
        if choice.lower() in possible_choices.lower():
            return choice.lower()
        print("Invalid option.")


def get_name():
    name = input("What is your name? ")
    return name


def get_card(possible_choices):
    success = False
    print(possible_choices)
    while not success:
        choice_str = input("> ")
        try:
            choice_int = int(choice_str)

            card = get_card_by_id(possible_choices, choice_int)
            if card:
                return choice_int
        except ValueError:
            pass
        print("Invalid card.")


def get_pile():
    success = False
    while not success:
        choice_str = input("> ")
        try:
            choice_int = int(choice_str)
            if choice_int in [0, 1, 2, 3]:
                return choice_int
        except ValueError:
            pass
        print("Invalid pile.")


def format_hand(card_list):
    if len(card_list) == 0:
        return " No cards"

    result = ""
    for card in card_list:
        result += f" {card['color']:5} - {card['number']:3}\n"

    return result


def display(game, name):
    user = game['user_list'][name]
    hand = user['hand']['card_list']
    hold = user['hold']['card_list']
    pile1 = user['pile1']['card_list']
    pile2 = user['pile2']['card_list']
    pile3 = user['pile3']['card_list']
    print(f"--> {name}")
    piles = pile1, pile2, pile3
    for i, pile in enumerate(piles):
        print(f"Pile {i + 1}  ", end="")
    print()

    row_count = max([len(pile) for pile in piles])
    for row in range(row_count):
        for pile in piles:
            if row < len(pile):
                print(f"{pile[row]:6}  ", end="")
        print()

    # print("Pile 1: ", format_hand(pile1))
    # print("Pile 2: ", format_hand(pile2))
    # print("Pile 3: ", format_hand(pile3))
    print()
    print("Hold:   ")
    print(format_hand(hold))
    print("Hand:   ")
    print(format_hand(hand))
    print()


def display_all(game, my_name):
    print(f"\nRound #{game['round']}")

    for user_name in game['user_list']:
        if user_name != my_name:
            display(game, user_name)

    display(game, my_name)


class GameUIText:

    def process_get_name_mode(self):
        print("Welcome!")
        print()
        self.name = get_name()
        self.mode = START_MODE

    def process_start_mode(self):
        print()
        print("C. Create Game")
        print("J. Join Game")
        print("Q. Quit")
        choice = get_choice("CJQ")
        if choice == 'c':
            result = create_game(server, self.name)
            assert result
            assert 'game_code' in result
            self.game_code = result['game_code']
            print(f"Game started. Your game code is '{self.game_code}'.")
            self.mode = LOBBY_MODE
        elif choice == 'j':
            game_code = input("Enter game code: ")
            result = join_game(server, game_code, self.name)
            if 'game_code' in result:
                self.game_code = result['game_code']
                self.mode = LOBBY_MODE

    def process_lobby_mode(self):
        print()
        print("V. View Lobby")
        print("S. Start Game")
        print("E. Exit Lobby")
        print("A. Add Computer Player")
        print("Q. Quit")
        choice = get_choice("VSEQA")
        if choice == 'e':
            self.mode = START_MODE
        elif choice == 'v':
            print("People in the lobby:")
            result = get_game(server, self.game_code)
            user_list = result['user_list']
            for user in user_list:
                print(user)
        elif choice == 's':
            result = start_game(server, self.game_code)
            if 'error' in result:
                print("Error:", result['error'])
            else:
                self.mode = PICK_FROM_HAND
        elif choice == 'a':
            result = add_computer_player(server, self.game_code)
            if 'error' in result:
                print("Error:", result['error'])

    def pick_from_hand(self):
        game = get_game(server, self.game_code)
        hand = game['user_list'][self.name]['hand']
        hold = game['user_list'][self.name]['hold']
        if len(hold) == 2:
            if game['mode'] == MODE_PICK_FROM_HAND:
                print("Waiting for other player...")
            elif game['mode'] == MODE_PICK_FROM_HOLD:
                print("Other players have finished picking from their hand.")
                self.mode = PICK_FROM_HOLD
            return

        display_all(game, self.name)
        print("Pick from hand:")

        card = get_card(hand)
        game = move_to_hold(server, self.game_code, self.name, card)
        if game['mode'] == MODE_PICK_FROM_HOLD:
            self.mode = PICK_FROM_HOLD

    def pick_from_hold(self):
        game = get_game(server, self.game_code)
        hold = game['user_list'][self.name]['hold']['card_list']
        if len(hold) == 0:
            if game['mode'] == MODE_PICK_FROM_HAND:
                self.mode = PICK_FROM_HAND
            else:
                print("Waiting for other player...")
            return

        display_all(game, self.name)
        print("Pick from hold...")

        card = get_card(hold)
        print("Pick pile 1...3 or 0 for discard:")
        pile = get_pile()
        game = move_to_pile(server, self.game_code, self.name, card, pile)
        if game['mode'] == MODE_PICK_FROM_HAND:
            self.mode = PICK_FROM_HAND

    def __init__(self):
        self.mode = GET_NAME_MODE
        self.name = None
        self.game_code = None

    def process(self):
        done = False

        while not done:
            if self.mode == START_MODE:
                self.process_start_mode()
            elif self.mode == GET_NAME_MODE:
                self.process_get_name_mode()
            elif self.mode == LOBBY_MODE:
                self.process_lobby_mode()
            elif self.mode == PICK_FROM_HAND:
                self.pick_from_hand()
            elif self.mode == PICK_FROM_HOLD:
                self.pick_from_hold()
