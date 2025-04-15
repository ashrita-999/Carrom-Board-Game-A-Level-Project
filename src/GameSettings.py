import tkinter
from PIL import ImageTk, Image


class GameSettings:
    def __init__(self, database, playernum):
        self.database = database
        self.playernum = playernum

        # create window object
        self.window = tkinter.Tk()
        self.window.title("Game Settings")
        # initialise tkinter window with dimensions
        self.window.geometry("620x280")

        # initialising the grid
        self.window.columnconfigure(0, weight=1, minsize=100)
        self.window.columnconfigure(1, weight=1, minsize=100)

        # creating dropdown box
        self.variable_gamemode = tkinter.StringVar(self.window)
        self.variable_gamemode.set(" ") #default value
        self.dpd_gamemode = tkinter.OptionMenu(self.window, self.variable_gamemode, 'Easy', 'Hard')

        self.variable_strikercolour = tkinter.StringVar(self.window)
        self.variable_strikercolour.set(" ") #default value
        self.dpd_strikercolour = tkinter.OptionMenu(self.window, self.strikercolour, 'Blue', 'Yellow', 'Orange', 'Green'
                                                    'Red', 'Black', 'White')
        # positioning dropdown boxes
        self.dpd_gamemode.grid(row=0, rowspan=1, column=1, columnspan=1, pady=5, sticky="ns")
        self.dpd_strikercolour.grid(row=1, rowspan=1, column=1, columnspan=1, pady=5, sticky="ns")

        # creating labels
        self.lbl_gamemode = tkinter.Label(self.window, width=100, text="Choose Game Difficulty")
        self.lbl_strikercolour = tkinter.Label(self.window, width=100, text="Choose Striker Colour")

        # positioning labels
        self.lbl_gamemode.grid(row=0, rowspan=1, column=0, columnspan=1, pady=5,  sticky="ns")
        self.lbl_strikercolour.grid(row=1, rowspan=1, column=0, columnspan=1, pady=5,  sticky="ns")

        # positioning entry boxes
        self.lbl_gamemode.grid(row=0, rowspan=1, column=0, columnspan=1, pady=5,  sticky="ns")
        self.lbl_strikercolour.grid(row=1, rowspan=1, column=0, columnspan=1, pady=5,  sticky="ns")

        btn = tkinter.Button(self.window, text="OK", width=100, command= self.play_game)
        btn.grid(row=2, column=0, columnspan=2, pady=5,  sticky="ns")


