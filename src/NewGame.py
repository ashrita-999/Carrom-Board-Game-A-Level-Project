import tkinter
from PlayerSettings import PlayerSettings


class NewGame:
    def __init__(self, database, game_window):
        self.database = database
        self.game_window = game_window
        # create window object
        self.window = tkinter.Tk()
        self.window.title("Create New Game")
        self.player_names = []

        # window colour
        self.window['background'] = '#E88C60'

        # initialise tkinter window with dimensions
        self.window.geometry("620x280")

        # initialising the grid
        self.window.columnconfigure(0, weight=1, minsize=100)
        self.window.columnconfigure(1, weight=1, minsize=100)

        # creating dropdown box
        self.variable = tkinter.StringVar(self.window)
        self.variable.set("2") #default value
        self.dpd_players = tkinter.OptionMenu(self.window, self.variable, '2', '4')
        self.dpd_players.config(bg = '#E88C60')

        # positioning dropdown box
        self.dpd_players.grid(row=0, rowspan=1, column=1, columnspan=1, pady=5, sticky="ns" )

        # creating labels
        lbl_players = tkinter.Label(self.window, width=100, text="Choose number of players", bg='#E88C60')

        # positioning labels
        lbl_players.grid(row=0, rowspan=1, column=0, columnspan=1, pady=5,  sticky="ns")

        #creating Next button
        btn1 = tkinter.Button(self.window, text="Next", width=100, command= self.read_players, highlightbackground='#E88C60')
        btn1.grid(row=1, column=0, columnspan=2, pady=5, sticky="ns")

    def read_players(self):
        #opening gamesettings window
        self.number_of_players = self.variable.get()
        print(self.number_of_players)
        PlayerSettings(self.database, self.number_of_players, self)



