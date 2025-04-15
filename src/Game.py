import tkinter


from GameWindow import GameWindow
from Database import Database


class Game:
    def __init__(self):
        self.database = Database()
        self.player_names = []
        self.game_window = GameWindow(self.database, self)
        self.game_window.show_main_window()


if __name__ == '__main__':
    Game()
