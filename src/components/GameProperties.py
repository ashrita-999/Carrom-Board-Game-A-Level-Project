

class GameProperties:
    def __init__(self, game_id, game_name="", game_mode="", striker_colour="", no_of_players=2, players=[], coins=[],
                 current_player=1):
        #saving game properties passed in into own attributes
        self.game_id = game_id
        self.game_name = game_name
        self.game_mode = game_mode
        self.striker_colour = striker_colour
        self.no_of_players = no_of_players

        #saving player points
        self.player_1_points = players[0]["score"]
        self.player_2_points = players[1]["score"]

        #player 3 and 4 points set to 0 if 2 player game
        self.player_3_points = players[2]["score"] if no_of_players == 4 else 0
        self.player_4_points = players[3]["score"] if no_of_players == 4 else 0

        #saving player names
        self.player_1 = players[0]["name"]
        self.player_2 = players[1]["name"]

        #player 3 and 4 set to null if 2 player game
        self.player_3 = "" if no_of_players == 2 else players[2]["name"]
        self.player_4 = "" if no_of_players == 2 else players[3]["name"]
        self.coins = coins
        self.players = players
        self.current_player = current_player

    def get_game_name(self):
        return self.game_name

    def get_game_mode(self):
        return self.game_mode

    def get_no_of_players(self):
        return self.no_of_players

    def get_players(self):
        return self.players

    def get_striker_colour(self):
        return self.striker_colour


