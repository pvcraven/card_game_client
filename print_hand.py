def print_hand(game, name):
    hand = game['user_list'][name]['hand']
    hold = game['user_list'][name]['hold']
    pile1 = game['user_list'][name]['pile1']
    pile2 = game['user_list'][name]['pile2']
    pile3 = game['user_list'][name]['pile3']
    print()
    print(name)
    print("Pile 1: ", pile1)
    print("Pile 2: ", pile2)
    print("Pile 3: ", pile3)
    print("Hold: ", hold)
    print("Hand: ", hand)
