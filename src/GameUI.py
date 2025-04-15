import pymunk.pygame_util
import pymunk
import pygame

from src.Database import Database
from src.components.Board import Board
from src.components.Button import Button
from src.components.CircularSlider import CircularSlider
from src.components.Coin import Coin
from src.components.Edges import Edges
from src.components.GameFunctions import GameFunctions
from src.components.GameProperties import GameProperties
from src.components.Slider import Slider
from src.components.EndGame import  EndGame


class GameUI:
    # set screen width and height
    SCREEN_WIDTH = 1366
    SCREEN_HEIGHT = 678

    def __init__(self, game_properties: GameProperties, database: Database):


        # defining game properties
        self.game_properties = game_properties
        self.database = database
        self.game_mode = self.game_properties.get_game_mode()
        self.game_name = self.game_properties.get_game_name()
        self.player_1_points = self.game_properties.player_1_points
        self.player_2_points = self.game_properties.player_2_points
        self.player_3_points = self.game_properties.player_3_points
        self.player_4_points = self.game_properties.player_4_points
        self.current_player = self.game_properties.current_player
        self.players = self.game_properties.get_players()
        self.noofplayers = self.game_properties.get_no_of_players()
        self.strikercolour = self.game_properties.get_striker_colour()

        # game window
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.imagepath = "/Users/ashri/git/carrom-board/src/assets/3.png"
        pygame.display.set_caption(self.game_name)

        # clock - defines how often the space is updated
        self.clock = pygame.time.Clock()
        self.FPS = 120  # screen is updated 120 times per second

        # colours
        self.BG = (50, 50, 50)  # background colour of screen

        # define properties of coins and create an array
        self.coin = []  # creates an array with all coins included
        self.properties = ((337, 300, "White", False), (337, 380, "White", False), (318, 330, "White", False), (372, 320, "White", False),
                      (337, 360, "White", False), (300, 361, "White", False), (300, 320, "White", False), (355, 329, "White", False),
                      (372, 360, "White", False), (337, 320, "Black", False), (318, 310, "Black", False) , (318, 350, "Black", False),
                      (318, 370, "Black", False), (300, 341, "Black", False), (355, 309, "Black", False), (355, 349, "Black", False),
                      (355, 369, "Black", False), (372, 340, "Black", False), (337, 340, "Red", False))

        # (337, 300, "white", False)
        # dimensions of edges
        self.edges = []  # array including all edges with positions as (x,y)
        self.edges_dimens = [
            [(65, 75), (65, 120), (608, 75), (608, 120)],  # top edge
            [(65, 565), (65, 605), (608, 565), (608, 605)],  # bottom edge
            [(65, 120), (110, 120), (65, 565), (110, 565)],  # lefthand edge
            [(563, 120), (563, 565), (608, 120), (608, 565)]  # righthand edge
        ]

        # dimensions of position slider
        self.slider_position_dimensions = (805, 75), (805, 120), (1348, 75), (1348, 120)
        self.slider_position_bar_dimensions = (805, 55), (805, 140), (815, 55), (815, 140)

        # dimensions of force slider
        self.slider_force_dimensions = (805, 175), (805, 220), (1348, 175), (1348, 220)
        self.slider_force_bar_dimensions = (805, 155), (805, 240), (815, 155), (815, 240)

        self.bar_dimensions = (805, 55), (805, 140), (815, 55), (815, 140)
        self.bar_dimensions2 = (805, 155), (805, 240), (815, 155), (815, 240)

        # Go button dimensions
        self.button_dimensions = (805, 255), (805, 340), (905, 255), (905, 340)

        # Save button dimensions
        self.save_button_dimensions = (1005, 255), (1005, 340), (1105, 255), (1105, 340)

        # circle base dimensions
        self.circle_base_dims = (805, 500)

        # circle base dimensions
        self.circle_slide_dim = (805, 500)

        # the space
        self.space = pymunk.Space()  # defines the shape in which Pymunk physics is applied
        self.static_body = self.space.static_body
        self.options = pymunk.pygame_util.DrawOptions(self.screen)
        self.options.flags = pymunk.SpaceDebugDrawOptions.DRAW_SHAPES  # shows only shapes, not constraints
        self.game_properties = game_properties

        # Error box for end game
        self.draw_alert = False
    def original_position(self, coins):
        count = 0
        bool = False
        for i in range(0,19):
            if (round(coins[i].body.position[0]), round(coins[i].body.position[1]) ) == (self.properties[i][0], self.properties[i][1]):
                #^ if coins are in middle of board (happens only at start of game)
                count = count + 1 #... count = count + 1
        if count == 18: #if all coins are in their starting position, function returns true (i.e. first strike hasn't happened yet)
            bool = True
        else:
            bool = False
        return bool

    def coins_moving(self, coins, strikercoin):
        # returns false only when all coins stop moving
        count = 0
        for i in range(0,19):
            if coins[i].get_holed() == False:
                if abs(coins[i].body.velocity[0]) > 5 or abs(coins[i].body.velocity[1]) > 5 or abs(strikercoin.body.velocity[0]) > 5 \
                        or abs(strikercoin.body.velocity[1]) > 5:
                    count = count + 1
        if count == 0:
            moving = False
        else:
            moving = True
        return moving


    def save_game(self):
        game = { "coins" : [] } #creating coin object
        for coin_i in self.coin:
            x = int(coin_i.body.position[0])
            y = int(coin_i.body.position[1])

            #appending all coin properties onto string
            coin = { "x": x, "y": y, "holed": coin_i.get_holed(), "colour": coin_i.colour }
            game["coins"].append(coin)

        #creating objects current_player and game_properties
        game["current_player"] = self.current_player_local
        game["game_properties"] = self.game_properties.__dict__

        #appending scores and players into game properties
        game["game_properties"]["players"][0]["score"]=self.newgame.get_player_1_points()
        game["game_properties"]["players"][1]["score"]=self.newgame.get_player_2_points()
        if self.noofplayers == 4:
            game["game_properties"]["players"][2]["score"]=self.newgame.get_player_3_points()
            game["game_properties"]["players"][3]["score"]=self.newgame.get_player_4_points()
        self.database.save_game(game)


    def start_game(self):
    #initialising

        pygame.display.init()

        #higher friction for harder game mode
        if self.game_mode == "Easy":
            max_force = 700
        else:
            max_force = 2000

        if len(self.game_properties.coins) > 0: # if game is existing
            # uses game properties to set x and y coordinates of each coin, and holed property
            for x in range(len(self.game_properties.coins)):
                coin = self.game_properties.coins[x]
                self.coin.append(Coin(coin["x"], coin["y"], 10, coin["colour"], self.static_body, self.space, max_force))
                self.coin[x].set_holed(coin["holed"])
                if self.coin[x].get_holed() == False:
                    self.coin[x].draw(self.space)
                self.coin[x].limit_velocity()

        else:
        #if game is a new game, passses in original coordinates and properties
            for x in range(19):
                self.coin.append(Coin(self.properties[x][0], self.properties[x][1], 10, self.properties[x][2], self.static_body, self.space, max_force))
                self.coin[x].draw(self.space)
                self.coin[x].set_holed(self.properties[x][3])
                self.coin[x].limit_velocity()

        striker_coin = Coin(x=490, y=590, coin_radius=14, colour=self.strikercolour, static_body=self.static_body, space=self.space, max_force=max_force)
        striker_coin.draw(self.space)
        striker_coin.set_holed(False)
        striker_coin.limit_velocity()


        # the edges
        for e in self.edges_dimens:
            self.edges.append(Edges(e, self.space))
        for i in range(4):
            self.edges[i].draw()

        #position slider
        sliderpos = Slider(self.slider_position_dimensions, self.slider_position_bar_dimensions, self.space)

        #force slider
        sliderforce = Slider(self.slider_force_dimensions, self.slider_force_bar_dimensions, self.space)

        #strike button
        Gobutton = Button(self.button_dimensions, self.space)

        #save game button
        save_button = Button(self.save_button_dimensions, self.space)

        #direction slider
        directionslider = CircularSlider(80, self.circle_base_dims, self.circle_slide_dim, 10, self.space)

        #alert box for end of game
        endgame = EndGame(self.screen)

        #configuring points
        if self.noofplayers ==4:
            team_1_points = self.player_1_points + self.player_3_points
            team_2_points = self.player_2_points + self.player_4_points
        else:
            team_1_points = self.player_1_points
            team_2_points = self.player_2_points

        #function for changing players and formulating points
        self.newgame = GameFunctions(current_player=0,
                                     noofplayers=self.noofplayers,
                                     team_1_points=team_1_points,
                                     team_2_points=team_2_points,
                                     current_player_colour='Black',
                                     current_team_points=0,
                                     player_1_points=self.player_1_points,
                                     player_2_points=self.player_2_points,
                                     player_3_points=self.player_3_points,
                                     player_4_points=self.player_4_points,
                                     sliderpos=sliderpos,
                                     sliderforce=sliderforce,
                                     directionslider=directionslider,
                                     StrikerCoin=striker_coin, Gobutton=Gobutton,
                                     game_properties=self.properties,
                                     button_dimensions=self.button_dimensions,
                                     circle_base_dims=self.circle_base_dims,
                                     CoinsMoving=self.coins_moving,
                                     space=self.space)

        #defining temporary variables
        self.current_player_local = self.current_player
        noofplayers_local = self.noofplayers
        change = False
        player_struck = False


        # event handler
        while True:
            self.clock.tick(self.FPS)  # defines how often the space updates
            self.space.step(1 / self.FPS)  # space-time moved in steps using this function
            self.newgame.perform_coin_in_hole(self.coin) # removes any coin that falls in hole
            # changeplayerbool = newgame.holed(coin, current_player_local)
            # fill bgd
            self.screen.fill(self.BG)
            if not self.coins_moving(self.coin, striker_coin) and player_struck and not self.original_position(self.coin) :
                # ^only performs the check once the coins have stopped moving, after a player has struck...
                # ... not originalposition(coin) : check does not happen before the first ever strike
                change = self.newgame.holed_check(self.coin, self.current_player_local) #if change is true, the player is changed
                player_struck = False # sets player_struck to false
                if change:
                    self.current_player_local = self.newgame.player_change(self.current_player_local) #changes player if change is true

                self.newgame.end_round(self.coin) #checks if round has ended

            # defines which alert box, if any, to render on the screen if the game is over
                end_game_output = self.newgame.end_game()
                if end_game_output == 1:
                    self.imagepath = "/Users/ashri/git/carrom-board/src/assets/1.png"
                    self.draw_alert = True
                elif end_game_output == 2:
                    self.imagepath = "/Users/ashri/git/carrom-board/src/assets/2.png"
                    self.draw_alert = True
                elif end_game_output == 3:
                    self.imagepath = "/Users/ashri/git/carrom-board/src/assets/3.png"
                    self.draw_alert = True
                elif end_game_output == 4:
                    self.imagepath = "/Users/ashri/git/carrom-board/src/assets/4.png"
                    self.draw_alert = True
                elif end_game_output == 0:
                    self.draw_alert = False

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN: #if mouse clicked
                    self.newgame.player_strike(self.current_player_local, self.coin, striker_coin) #changes slider positions and strikes coin
                    if Gobutton.CheckClicked(self.button_dimensions) == 'True': # if go button is clicked
                        player_struck = True #player struck set to true

                #saves game if save button clicked
                    if save_button.CheckClicked(self.save_button_dimensions) == 'True':
                        self.save_game()
                if event.type == pygame.QUIT:
                    return

            #rendering images
            board = Board(self.screen)
            board.draw()
            Gobutton.draw(self.screen, "/Users/ashri/git/carrom-board/src/assets/Screenshot 2023-03-18 at 13.48.47.png", 100, 50, 805, 335 )
            save_button.draw(self.screen, "/Users/ashri/git/carrom-board/src/assets/Screenshot 2023-03-18 at 13.52.14.png", 100, 50, 1005, 335)
            endgame.draw(self.screen, self.imagepath, 300, 300, 1005, 385, self.draw_alert)
            sliderforce.draw(self.screen, "/Users/ashri/git/carrom-board/src/assets/Screenshot 2023-03-18 at 13.59.15.png", 100, 50, 705, 170)
            sliderpos.draw(self.screen, "/Users/ashri/git/carrom-board/src/assets/Screenshot 2023-03-18 at 13.59.20.png", 100, 50, 705, 70)

            self.space.debug_draw(self.options)
            pygame.display.update()



