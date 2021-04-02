import os

file_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(file_path)

from game_ui_text import GameUIText


def main():
    game_ui = GameUIText()
    game_ui.process()


main()
