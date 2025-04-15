import tkinter
from PIL import ImageTk, Image


class ReadPlayer:
    def __init__(self, database, player, new_game):
        self.database = database
        self.new_game = new_game
        # create window object
        self.window = tkinter.Tk()
        self.window.title("Player - " + str(player))

        # initialise tkinter window with dimensions
        self.window.geometry("620x280")

        # initialising the grid
        self.window.columnconfigure(0, weight=1, minsize=100)
        self.window.columnconfigure(1, weight=1, minsize=100)

        # creating entry boxes
        self.ebox_players = tkinter.Entry(self.window,  width=100)

        # positioning entry boxes
        self.ebox_players.grid(row=0, rowspan=1, column=1, columnspan=1, pady=5, sticky="ns")

        # creating labels
        lbl_players = tkinter.Label(self.window, width=100, text="Enter user name for player " + str(player))

        # positioning entry boxes
        lbl_players.grid(row=0, rowspan=1, column=0, columnspan=1, pady=5,  sticky="ns")

        btn = tkinter.Button(self.window, text="OK", width=100, command= self.read_players)
        btn.grid(row=1, column=0, columnspan=2, pady=5,  sticky="ns")

    def read_players(self):
        self.new_game.game_window.game.player_names.append(self.ebox_players.get())
        self.database.create_user(self.ebox_players.get())
        self.window.destroy()

