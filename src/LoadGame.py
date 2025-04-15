import json
import tkinter

import pygame

from src.GameUI import GameUI
from src.components.GameProperties import GameProperties


class LoadGame:
    def __init__(self, database, game_window):
        self.database = database
        self.game_window = game_window
        # create window object
        self.window = tkinter.Tk()
        self.window.title("Load Previous Game")
        self.window['background'] = '#E88C60'

        #label players
        lbl_players = tkinter.Label(self.window, width=100, text="Choose saved game", bg='#E88C60')
        lbl_players.grid(row=0, column=0, columnspan=1, pady=5,  sticky="ns")


        # initialise tkinter window with dimensions
        self.window.geometry("620x280")

        # initialising the grid
        self.window.columnconfigure(0, weight=1, minsize=100)
        self.window.columnconfigure(1, weight=1, minsize=100)

        # creating dropdown box
        self.variable_game_data = tkinter.StringVar(self.window)
        self.variable_game_data.set("MyCarromBoard") #default value
        game_names = self.database.get_game_names()

        self.dpd_game_names = tkinter.OptionMenu(self.window, self.variable_game_data, *game_names)
        self.dpd_game_names.config(bg='#E88C60')

        # positioning dropdown box
        self.dpd_game_names.grid(row=0, column=1, columnspan=1, pady=5, sticky="ns")


        #creating Next button
        btn = tkinter.Button(self.window, text="Next", width=100, command= self.load_game, highlightbackground='#E88C60')
        btn.grid(row=1, column=0, columnspan=2, pady=5,  sticky="ns")

    def load_game(self):
        #entry from dropdown box
        game_data = self.variable_game_data.get()

        # uses game_id – (game_data)[0] – to load game details
        game_details = self.database.get_game_data(eval(game_data)[0])

        # passes in game details as parameters to GameProperties using properties in game_details
        json_game_data = json.loads(game_details)
        json_game_properties = json_game_data["game_properties"]
        game_properties = GameProperties(game_id=json_game_properties["game_id"],
                                         game_name=json_game_properties["game_name"],
                                         game_mode=json_game_properties["game_mode"], coins=json_game_data["coins"],
                                         striker_colour=json_game_properties["striker_colour"],
                                         no_of_players=json_game_properties["no_of_players"],
                                         players=json_game_properties["players"],
                                         current_player=json_game_properties["current_player"])
        load_game = GameUI(game_properties, self.database)
        load_game.start_game()
        pygame.display.quit()
        print(game_properties)




