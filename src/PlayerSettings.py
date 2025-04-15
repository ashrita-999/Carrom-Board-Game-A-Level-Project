import tkinter

import pygame.display

from src.GameUI import GameUI
# from src.GameUI import GameUI
from src.components.GameProperties import GameProperties

from tkinter import messagebox

class PlayerSettings:
    def __init__(self, database, no_of_players, new_game):
        self.database = database
        self.new_game = new_game
        self.no_of_players = int(no_of_players)

        # create window object
        self.window = tkinter.Tk()
        self.window.title("Player Settings")
        label_place = "e"
        self.window['background'] = '#E88C60'

        # initialise tkinter window with dimensions
        self.window.geometry("620x280")

        # initialising the grid
        self.window.columnconfigure(0, weight=1, minsize=100)
        self.window.columnconfigure(1, weight=1, minsize=100)

        # creating labels
        lbl_game_name = tkinter.Label(self.window, width=100, text="Game Name:", bg='#E88C60')
        # positioning entry boxes
        lbl_game_name.grid(row=0, rowspan=1, column=0, columnspan=1, pady=5, sticky=label_place)
        # creating entry boxes
        self.ebox_game_name = tkinter.Entry(self.window, width=100, highlightbackground='#E88C60')
        # positioning entry boxes
        self.ebox_game_name.grid(row=0, rowspan=1, column=1, columnspan=1, pady=5, sticky="ns")

        # creating components for striker color
        lbl_striker_color = tkinter.Label(self.window, width=100, text="Striker Colour:", bg='#E88C60')
        lbl_striker_color.grid(row=1, rowspan=1, column=0, columnspan=1, pady=5, sticky=label_place)

        self.variable_striker_colour = tkinter.StringVar(self.window)
        self.variable_striker_colour.set(" ")  # default value
        self.dpd_striker_colour = tkinter.OptionMenu(self.window, self.variable_striker_colour, 'Blue', 'Yellow',
                                                     'Orange', 'Green', 'Red', 'Black', 'White')
        self.dpd_striker_colour.grid(row=1, rowspan=1, column=1, columnspan=1, pady=5, sticky="w")
        self.dpd_striker_colour.config(bg='#E88C60')

        # creating components for game mode
        self.variable_game_mode = tkinter.StringVar(self.window)
        self.variable_game_mode.set(" ")  # default value

        lbl_game_mode = tkinter.Label(self.window, width=100, text="Game Difficulty:", bg='#E88C60')
        lbl_game_mode.grid(row=2, rowspan=1, column=0, columnspan=1, pady=5, sticky=label_place)
        self.dpd_game_mode = tkinter.OptionMenu(self.window, self.variable_game_mode, 'Easy', 'Hard')
        self.dpd_game_mode.grid(row=2, rowspan=1, column=1, columnspan=1, pady=5, sticky="w")
        self.dpd_game_mode.config(bg='#E88C60')

        self.show_players()
        button_row = 5 if self.no_of_players == 2 else 7
        btn = tkinter.Button(self.window, text="OK", width=100, command=self.read_players, highlightbackground='#E88C60')
        btn.grid(row=button_row, column=0, columnspan=2, pady=5, sticky="ns")

    def show_players(self):
        # creating labels
        lbl_player_1 = tkinter.Label(self.window, width=100, text="Username (player 1):", bg='#E88C60')
        # positioning entry boxes
        lbl_player_1.grid(row=3, rowspan=1, column=0, columnspan=1, pady=5, sticky="e")

        # creating entry boxes
        self.ebox_player_1 = tkinter.Entry(self.window, width=100, highlightbackground='#E88C60')
        # positioning entry boxes
        self.ebox_player_1.grid(row=3, rowspan=1, column=1, columnspan=1, pady=5, sticky="ns")

        # creating labels
        lbl_player_2 = tkinter.Label(self.window, width=100, text="Username (player 2):", bg='#E88C60')
        # positioning entry boxes
        lbl_player_2.grid(row=4, rowspan=1, column=0, columnspan=1, pady=5, sticky="e")

        # creating entry boxes
        self.ebox_player_2 = tkinter.Entry(self.window, width=100, highlightbackground='#E88C60')
        # positioning entry boxes
        self.ebox_player_2.grid(row=4, rowspan=1, column=1, columnspan=1, pady=5, sticky="ns")

        if (self.no_of_players == 4):
            # creating labels
            lbl_player_3 = tkinter.Label(self.window, width=100, text="Username (player 3):", bg='#E88C60')
            # positioning entry boxes
            lbl_player_3.grid(row=5, rowspan=1, column=0, columnspan=1, pady=5, sticky="e")

            # creating entry boxes
            self.ebox_player_3 = tkinter.Entry(self.window, width=100, highlightbackground='#E88C60')
            # positioning entry boxes
            self.ebox_player_3.grid(row=5, rowspan=1, column=1, columnspan=1, pady=5, sticky="ns")

            # creating labels
            lbl_player_4 = tkinter.Label(self.window, width=100, text="Username (player 4):", bg='#E88C60')
            # positioning entry boxes
            lbl_player_4.grid(row=6, rowspan=1, column=0, columnspan=1, pady=5, sticky="e")

            # creating entry boxes
            self.ebox_player_4 = tkinter.Entry(self.window, width=100, highlightbackground='#E88C60')
            # positioning entry boxes
            self.ebox_player_4.grid(row=6, rowspan=1, column=1, columnspan=1, pady=5, sticky="ns")


    def validation(self):
        validated = True
    #validating game name
        game_names = self.database.get_game_names()
        for game in game_names:
            if game == (self.ebox_game_name.get(),):
                tkinter.messagebox.showerror("Error", "That game already exists")
                validated = False
    #checking if all usernames are unique
        if self.no_of_players ==2:
            if self.ebox_player_1.get() == self.ebox_player_2.get():
                tkinter.messagebox.showerror("Error", "The usernames must all be unique")
                validated = False
        else:
            message = []
            message.extend([self.ebox_player_1.get(),self.ebox_player_2.get(), self.ebox_player_3.get(),
                            self.ebox_player_4.get()])
            count = 0
            bool = False
            for i in range(0,4):
                item = message[i]
                for j in range(0,4):
                    if item == message[j] and j != i:
                        count = count + 1
            if count > 0:
                bool = True
            if bool == True:
                tkinter.messagebox.showerror("Error", "The usernames must all be unique")
                validated = False

        # checking if values have been entered into the player boxes
        if self.ebox_player_1.get() == "" or self.ebox_player_2.get() == "":
            tkinter.messagebox.showerror("Error", "You must enter a username")
            validated = False
        if self.no_of_players == 4:
            if self.ebox_player_3.get() == "" or self.ebox_player_4 == "":
                tkinter.messagebox.showerror("Error", "You must enter a username")
                validated = False

        # checking if values have been entered into the game box
        if self.ebox_game_name == "" :
            tkinter.messagebox.showerror("Error", "You must enter a game name")
            validated = False

        # checking if any usernames match existing ones, and displaying an alert box if they do
        user_names = self.database.get_user_names()
        for user in user_names:

            if user == (self.ebox_player_1.get(),):
                msg_box = tkinter.messagebox.askyesno(None, "Careful, Username1 already exists. Is this you?")
                if msg_box == True:
                    validated = True
                else:
                    validated = False
            if user == (self.ebox_player_2.get(),):
                msg_box = tkinter.messagebox.askyesno(None, "Careful, Username2 already exists. Is this you?")
                if msg_box == True:
                    validated = True
                else:
                    validated = False
            if self.no_of_players == 4:

                if user == (self.ebox_player_3.get(),):
                    msg_box = tkinter.messagebox.askyesno(None, "Careful, Username3 already exists. Is this you?")
                    if msg_box == True:
                        validated = True
                    else:
                        validated = False
                if user == (self.ebox_player_4.get(),):
                    msg_box = tkinter.messagebox.askyesno(None, "Careful, Username4 already exists. Is this you?")
                    if msg_box == True:
                        validated = True
                    else:
                        validated = False

        return(validated)



    def read_players(self):

        #gets game details
        game_name = self.ebox_game_name.get()
        striker_colour = self.variable_striker_colour.get()
        game_mode = self.variable_game_mode.get()
        player_names = [self.ebox_player_1.get(), self.ebox_player_2.get()]
        players = [{"name": self.ebox_player_1.get(), "score": 0}, {"name": self.ebox_player_2.get(), "score": 0}]
        if self.no_of_players == 4:
            players.append({"name": self.ebox_player_3.get(), "score": 0})
            players.append({"name": self.ebox_player_4.get(), "score": 0})


        validated = self.validation()
        if validated == True:

            #passes in game details to database using create_game method
            game_id = self.database.create_game(game_name=game_name, no_of_players=self.no_of_players,
                                                striker_color=striker_colour, game_difficulty=game_mode,
                                                player_names=player_names)
            self.new_game.window.destroy()
            self.window.destroy()

            #opening game using above variables
            game_properties = GameProperties(game_id, game_name, game_mode, striker_colour, self.no_of_players,
                                             players, [])
            load_game = GameUI(game_properties, self.database)
            load_game.start_game()
            pygame.display.quit()
