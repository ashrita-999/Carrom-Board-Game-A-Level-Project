import pymunk.pygame_util
import pygame
import pymunk
import math

# INITIAL CODE
pygame.init()
GAME_FONT = pygame.font.SysFont('Comic Sans MS', 30)

# set screen width and height
SCREEN_WIDTH = 1366
SCREEN_HEIGHT = 678

# game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Play Carrom!")

# the space
space = pymunk.Space()  # defines the shape in which Pymunk physics is applied
static_body = space.static_body
options = pymunk.pygame_util.DrawOptions(screen)
options.flags = pymunk.SpaceDebugDrawOptions.DRAW_SHAPES  # shows only shapes, not constraints

# clock - defines how often the space is updated
clock = pygame.time.Clock()
FPS = 600  # screen is updated 120 times per second


# colours
BG = (50, 50, 50)  # background colour of screen

# define properties of coins and create an array
coin = []  # creates an array with all coins included
properties = ((337, 300, "white", False), (337, 380, "white", False), (318, 330, "white", False), (372, 320, "white", False),
              (337, 360, "white", False), (300, 361, "white", False), (300, 320, "white", False), (355, 329, "white", False),
              (372, 360, "white", False), (337, 320, "black", False), (318, 310, "black", False) , (318, 350, "black", False),
              (318, 370, "black", False), (300, 341, "black", False), (355, 309, "black", False), (355, 349, "black", False),
              (355, 369, "black", False), (372, 340, "black", False), (337, 340, "red", False))

# (337, 300, "white", False)
# dimensions of edges
edges = []  # array including all edges with positions as (x,y)
edges_dimens = [
    [(65, 75), (65, 120), (608, 75), (608, 120)],  # top edge
    [(65, 565), (65, 605), (608, 565), (608, 605)],  # bottom edge
    [(65, 120), (110, 120), (65, 565), (110, 565)],  # lefthand edge
    [(563, 120), (563, 565), (608, 120), (608, 565)]  # righthand edge
]

# dimensions of position slider
slider_position_dimensions = (805, 75), (805, 120), (1348, 75), (1348, 120)
slider_position_bar_dimensions = (805, 55), (805, 140), (815, 55), (815, 140)

# dimensions of force slider
slider_force_dimensions = (805, 175), (805, 220), (1348, 175), (1348, 220)
slider_force_bar_dimensions = (805, 155), (805, 240), (815, 155), (815, 240)

bar_dimensions = (805, 55), (805, 140), (815, 55), (815, 140)
bar_dimensions2 = (805, 155), (805, 240), (815, 155), (815, 240)

# button dimensions
button_dimensions = (805, 255), (805, 340), (905, 255), (905, 340)

# circle base dimensions
circle_base_dims = (805, 500)

# circle base dimensions
circle_slide_dim = (805, 500)



def originalposition(coins):
    count = 0
    bool = False
    for i in range(0,19):
        if (round(coins[i].body.position[0]), round(coins[i].body.position[1]) ) == (properties[i][0], properties[i][1]):
            #^ if coins are in middle of board (happens only at start of game)
            count = count + 1 #... count = count + 1
    if count == 18: #if all coins are in their starting position, function returns true (i.e. first strike hasn't happened yet)
        bool = True
    else:
        bool = False
    return bool



class Coin:
    def __init__(self, x, y, coin_radius, colour):
        self.body = pymunk.Body()  # defines the coin as a pymunk body
        self.body.position = x, y  # takes in x,y coords to position the body on the screen
        self.coin_radius = coin_radius  # takes in argument coin_radius to set the size of the coin
        self.shape = pymunk.Circle(self.body, coin_radius)  # sets the shape of the coin as a circle
        self.colour = colour
        if colour == "red":
            self.shape.color = (255, 80, 100, 255)  # makes the coin red
        elif colour == "white":
            self.shape.color = (255, 255, 255, 255)  # makes the coin white
        elif colour == "black":
            self.shape.color = (0, 0, 0, 0)  # makes the coin black
        self.shape.mass = 5  # unitless mass for coin
        self.pivot = pymunk.PivotJoint(static_body, self.body, (0, 0), (0, 0))  # using pivot joint for friction
        self.pivot.max_bias = 0  # disables joint correction
        self.pivot.max_force = 1000  # emulates linear friction
        self.shape.elasticity = 0.8
        space.add(self.body, self.shape, self.pivot)  # adds the coin to the screen
        self.holed = False
        self.holed_temp = False

    def limit_velocity(self):
        max_velocity = 1000
        pymunk.Body.update_velocity(self.body, (0,0), 1, 1)
        l = self.body.velocity.length
        if l > max_velocity:
            scale = max_velocity / l
            self.body.velocity = self.body.velocity * scale


    def changePos(self, slider, current_player):
        self.player = current_player
        if self.player == 1: #bottom player
            x =  (194 + (((slider.current_dimensions.central_value - 805) / 547) * 283)) #gets the new y-coordinate of striker using position slider
            y = 490
        elif self.player == 2: #next player clockwise (right-side player)
            x = 488
            y = (200 + (((slider.current_dimensions.central_value - 805) / 555) * 283)) #gets the new y-coordinate of striker using position slider
        elif self.player == 3: #topmost player
            x =  (194 + (((slider.current_dimensions.central_value - 805) / 547) * 283)) #gets the new x-coordinate of striker using position slider
            y = 191
        elif self.player == 4: #left-hand side player
            x = 186
            y = (200 + (((slider.current_dimensions.central_value - 805) / 555) * 283)) #gets the new x-coordinate of striker using position slider
        else:
            x =  (194 + (((slider.current_dimensions.central_value - 805) / 547) * 283)) #gets the new y-coordinate of striker using position slider
            y = 490
        self.body.position = x, y #changes the position of the striker to the x and y values specified

    def moveStriker(self, forcer, angle, centrepoint):
        force = 1 * (((forcer.current_dimensions.central_value - 805) / 543) * 283)*80 # uses the force slider to calculate value of force
        # x = force *  math.cos(angle.current_dimensions.central_value)
        # y = force *  math.sin(angle.current_dimensions.central_value)
        x = 0
        y = 0
        xfixed = centrepoint[0]
        yfixed = centrepoint[1]
        xslider = angle.current_dimensions.slidebar_dimensions[0]
        yslider = angle.current_dimensions.slidebar_dimensions[1]
        if xslider - xfixed > 0 :
            x = force *  math.cos(angle.current_dimensions.central_value)
        elif xslider - xfixed < 0 :
            x = -(force *  math.cos(angle.current_dimensions.central_value))
        if yslider - yfixed > 0 :
            y = force *  math.sin(angle.current_dimensions.central_value)
        elif yslider - yfixed < 0 :
            y = -(force *  math.sin(angle.current_dimensions.central_value))
        self.body.apply_impulse_at_local_point((x, y), (0, 0)) #applies an impulse using the force specified

    def set_holed(self, holed):
        self.holed = holed

    def get_holed(self):
        return(self.holed)

    def set_holed_temp(self, tempholed):
        self.holed_temp = tempholed

    def get_holed_temp(self):
        return (self.holed_temp)

    def if_holed(self):
        bool = False
        x = self.body.position[0] # the x-coordinate of the coin's position
        y = self.body.position[1] # the y-coordinate of the coin's position
        if math.pow(x-542,2) + math.pow(y-134,2) <= math.pow(18,2) \
                or math.pow(x-123,2) + math.pow(y-132,2) <= math.pow(18,2)\
                or math.pow(x-123,2) + math.pow(y-551,2) <= math.pow(18,2) \
                or math.pow(x-551,2) + math.pow(y-549,2) <= math.pow(18,2): #if the coin lies within any of the holes, bool set to true
            bool = True
        return(bool) #bool is only true if the coin's velocity is 0 and is in the hole (i.e., coin is holed)

    def getColour(self):
        return(self.colour)

    def remove(self):
        space.remove(self.body, self.shape, self.pivot)

    def resetPosition(self,x,y):
        self.body.position = x,y
        self.body.velocity = (0, 0)
        space.add(self.body, self.shape, self.pivot)

    def setVelocity(self):
        self.body.velocity = (0,0)




class Board:
    def __init__(self):
        self.table_image = pygame.image.load(
            "/Users/ashri/git/carrom-board/src/assets/nusry-n-0RIEyCTxz4I-unsplash.jpg").convert_alpha()
        #  load image
        self.table_imagereal = pygame.transform.scale(self.table_image, (678, 678))
        #  scales image to board size

    def draw(self):
        screen.blit(self.table_imagereal, (0, 0))
        # draws carrom board on the screen


class Edges:
    def __init__(self, dimens):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = ((0, 0))
        self.shape = pymunk.Poly(self.body, dimens)
        self.shape.elasticity = 0.8

    def draw(self):
        space.add(self.body, self.shape)


class GameDimension: # This is a utility class used for getting the multiple properties of get_dimensions
    def __init__(self, slidebar_dimensions, central_value):
        self.slidebar_dimensions = slidebar_dimensions
        self.central_value = central_value


def CoinsMoving(coins, strikercoin):
    count = 0
    for i in range(0,19):
        if coins[i].get_holed() == False:
            if coins[i].body.velocity[0] > 5 or coins[i].body.velocity[1] > 5 or strikercoin.body.velocity[0] > 5 \
                    or strikercoin.body.velocity[1] > 5:
                count = count + 1
    if count == 0:
        moving = False
    else:
        moving = True
    return moving


class Button:
    def __init__(self, dimens):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = ((0, 0))
        self.shape = pymunk.Poly(self.body, dimens)
        space.add(self.body, self.shape)

    def CheckClicked(self, initial_dimensions):
        mouse_pos = pygame.mouse.get_pos()
        if initial_dimensions[0][0] < mouse_pos[0] < initial_dimensions[2][0] and initial_dimensions[1][1] > mouse_pos[
            1] > initial_dimensions[2][1]:
            return ('True')
        else:
            return ('False')

class Slider:
    def __init__(self, dimensions_base, dimensions_bar):
        self.initial_dimensions = dimensions_base # sets dimensions of base of slider
        self.slide_base = pymunk.Body(body_type=pymunk.Body.STATIC) # sets slider base to a static object
        self.slide_base.position = ((0, 0))
        self.slide_bar_holder_shape = pymunk.Poly(self.slide_base, self.initial_dimensions) #sets slider base as 'poly' (4 vertices)
        space.add(self.slide_base, self.slide_bar_holder_shape) #adds slider base to the space

        self.initial_bar_dimensions = dimensions_bar # sets dimensions of sliding bar
        self.slide_bar = pymunk.Body(body_type=pymunk.Body.STATIC) # sets sliding bar as a static body
        self.slide_bar.position = ((0, 0))
        self.current_dimensions = self.get_dimensions() # current_dimensions is used instead of a global variable to be able to move the striker (used in coin.changePos)
        self.dimens_bar = self.current_dimensions.slidebar_dimensions # sets dimens_bar to the current position of sliding bar using current_dimensions attribute
        self.slide_bar_shape = pymunk.Poly(self.slide_bar, self.dimens_bar) # sets sliding bar shape as a 'Poly' (4 vertices)
        self.slide_bar_shape.color = (255, 80, 100, 255) #sets colour of sliding bar to red
        space.add(self.slide_bar, self.slide_bar_shape) #adds sliding bar to the screen

    def move(self):
        mouse_pos = pygame.mouse.get_pos() #mouse_pos set to x and y coordinates of the current mouse position
        if self.initial_dimensions[0][0] < mouse_pos[0] < self.initial_dimensions[2][0] \
                and self.initial_dimensions[1][1] > mouse_pos[1] > self.initial_dimensions[2][1]  :
            space.remove(self.slide_bar, self.slide_bar_shape) # removes previous instances of the sliding bar
            self.dimens_bar = self.get_dimensions().slidebar_dimensions # sets the dimensions of the bar using the get_dimensions method
            self.slide_bar_shape = pymunk.Poly(self.slide_bar, self.dimens_bar) # sets sliding bar as a 'Poly' shape (4 vertices)
            self.slide_bar_shape.color = (255, 80, 100, 255) # sets sliding bar's colour to red
            space.add(self.slide_bar, self.slide_bar_shape) #adds new instance of sliding bar to the screen

    def get_dimensions(self):
        mouse_pos = pygame.mouse.get_pos() #gets the mouse position of the screen
        mouse_x = mouse_pos[0] #sets mouse_x to the x-coordinate of mouse-position
        y = (self.initial_dimensions[0][1] + self.initial_dimensions[1][1]) / 2
        x = mouse_pos[0]
        avgx = (self.initial_bar_dimensions[2][0] - self.initial_bar_dimensions[0][0]) / 2
        avgy = (self.initial_bar_dimensions[1][1] - self.initial_bar_dimensions[0][1]) / 2
        slider_bar_dimens = (x - avgx, y + avgy), (x - avgx, y - avgy), (x + avgx, y + avgy), (x + avgx, y - avgy)
        self.current_dimensions = GameDimension(slider_bar_dimens, mouse_x) # uses the GameDimension utility class to return slider_bar_dimens and mouse_x both
        return self.current_dimensions


class Circular_Slider:
    def __init__(self, base_radius, position_circle_base, position_circle_slide, circle_slide_radius):
        self.circle_base_position = position_circle_base
        self.circle_slide_base = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.circle_slide_base.position = ((self.circle_base_position[0], self.circle_base_position[1]))
        self.base_radius = base_radius
        self.slide_bar_holder_shape = pymunk.Circle(self.circle_slide_base, base_radius)
        space.add(self.circle_slide_base, self.slide_bar_holder_shape)

        self.circle_base_position = position_circle_base
        self.circle_slide_base2 = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.circle_slide_base2.position = ((self.circle_base_position[0], self.circle_base_position[1]))
        self.base_radius2 = base_radius - 8
        self.slide_bar_holder_shape2 = pymunk.Circle(self.circle_slide_base2, self.base_radius2)
        self.slide_bar_holder_shape2.color = (50, 50, 50, 50)
        space.add(self.circle_slide_base2, self.slide_bar_holder_shape2)

        self.circle_bar_position = position_circle_slide
        self.circle_slide = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.current_dimensions = self.get_position()
        self.posit_circle_slide = self.current_dimensions.slidebar_dimensions
        self.circle_slide.position = ((self.posit_circle_slide[0], self.posit_circle_slide[1]))
        self.circle_slide_radius = circle_slide_radius
        self.circle_slide_shape = pymunk.Circle(self.circle_slide, self.circle_slide_radius)
        self.circle_slide_shape.color = (255, 80, 100, 255)
        space.add(self.circle_slide, self.circle_slide_shape)

    def move(self):
        mouse_pos = pygame.mouse.get_pos()
        x1 = self.circle_base_position[0]
        y1 = self.circle_base_position[1]
        x = mouse_pos[0] - x1
        y = mouse_pos[1] - y1
        if math.pow(x,2) + math.pow(y,2) < math.pow(self.base_radius, 2) or math.pow(x,2) + math.pow(y,2) == math.pow(self.base_radius, 2) :
            space.remove(self.circle_slide, self.circle_slide_shape)
            self.posit_circle_slide = self.get_position().slidebar_dimensions
            self.circle_slide.position = ((self.posit_circle_slide[0], self.posit_circle_slide[1]))
            self.circle_slide_shape = pymunk.Circle(self.circle_slide, self.circle_slide_radius)
            self.circle_slide_shape.color = (255, 80, 100, 255)
            space.add(self.circle_slide, self.circle_slide_shape)


    def get_position(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_x = mouse_pos[0]
        mouse_y = mouse_pos[1]
        x1 = self.circle_base_position[0]
        y1 = self.circle_base_position[1]
        angle = abs(math.atan((mouse_y - y1 ) / (mouse_x - x1)))
        if mouse_x - x1 < 0:
            self.xpos =  x1 - self.base_radius*math.cos(angle)
        else :
            self.xpos = self.base_radius*math.cos(angle) + x1
        if mouse_y - y1 < 0:
            self.ypos = y1 - self.base_radius*math.sin(angle)
        else:
            self.ypos = y1 + self.base_radius*math.sin(angle)
        circle_slide_position = (self.xpos, self.ypos)
        self.current_dimensions = GameDimension(circle_slide_position, angle)
        return self.current_dimensions


# class Points():
#     def __init__(self):
#         self.team_1_points() = team_1_points
#         self.team_2_points() = team_2_points
#         Team_1_points = 0
#         Team_2_points = 0
#         Player_1_points = 0
#         Player_2_points = 0
#         Player_3_points = 0
#         Player_4_points = 0
#         current_team_points = 0
#         current_player_colour  = 'black'
#         current_player = 1
#         noofplayers = 4

# def playe
#
#
def player_strike(sliderpos, sliderforce, directionslider, StrikerCoin, Gobutton, current_player_loc):
    sliderpos.move()
    sliderforce.move()
    directionslider.move()
    StrikerCoin.changePos(sliderpos, current_player_loc)
    if Gobutton.CheckClicked(button_dimensions) == ('True'):
        StrikerCoin.moveStriker(sliderforce, directionslider, circle_base_dims)


class Gamefunc():
    def __init__(self, current_player, noofplayers, team_1_points, team_2_points, current_player_colour,
                 current_team_points, player_1_points, player_2_points, player_3_points, player_4_points,
                 sliderpos, sliderforce, directionslider, StrikerCoin, Gobutton):
        self.current_player = current_player # the player that has just struck
        self.noofplayers = noofplayers # total number of players
        self.team_1_points = team_1_points # points for team 1
        self.team_2_points = team_2_points # points for team 2
        self.current_player_colour = current_player_colour # coin colour of current player
        self.current_team_points = current_team_points # number of points for current team after most recent strike (holds temporary values)
        # player points below: total points for each individual player (only used when 4 players)
        self.player_1_points = player_1_points
        self.player_2_points = player_2_points
        self.player_3_points = player_3_points
        self.player_4_points = player_4_points
        self.sliderpos = sliderpos #position slider
        self.sliderforce = sliderforce #force slider
        self.directionslider = directionslider #circular direction slider
        self.StrikerCoin = StrikerCoin #striker
        self.Gobutton = Gobutton # button to strike
        self.red_hit = False # if a red coin has been hit or not
        self.noofcoinsonboard = 18 #total number of coins on board

    def player_change(self, current_player):
        self.current_player = current_player
        if self.noofplayers == 2 : # if there are 2 players
            if self.current_player == 1 : #if current player is 1 (bottommost)
                self.team_1_points = self.team_1_points + self.current_team_points
                #^team 1 points increases by total number of points won after most recent strike
                self.current_player = 3 # current player goes to topmost player
                self.current_player_colour = 'white' #current player colour is white
                self.current_team_points = 0 # current team points set to 0
            elif self.current_player ==3 : # if current player is 3 (topmost)
                self.team_2_points = self.team_2_points + self.current_team_points
                #^team 2 points increases by total number of points won after most recent strike
                self.current_team_points = 0 # current team points set to 0
                self.current_player = 1 # current player goes to bottommost player
                self.current_player_colour = 'black'
            elif current_player == 0:
                self.current_player = 1
                self.current_team_points = 0
                self.current_player_colour = 'black'

        if self.noofplayers == 4:
            if self.current_player == 1 :
                self.team_1_points = self.team_1_points + self.current_team_points
                self.player_1_points = self.player_1_points + self.current_team_points
                self.current_team_points = 0
                self.current_player = 2
                self.current_player_colour = 'white'
            elif self.current_player == 2 :
                self.team_2_points = self.team_2_points + self.current_team_points
                self.player_2_points = self.player_2_points + self.current_team_points
                self.current_team_points = 0
                self.current_player = 3
                self.current_player_colour = 'black'
            elif self.current_player == 3:
                self.team_1_points = self.team_1_points + self.current_team_points
                self.player_3_points = self.player_3_points + self.current_team_points
                self.current_team_points = 0
                self.current_player = 4
                self.current_player_colour = 'white'
            elif self.current_player == 4:
                self.team_2_points = self.team_2_points + self.current_team_points
                self.player_4_points = self.player_4_points + self.current_team_points
                self.current_team_points = 0
                self.current_player = 1
                self.current_player_colour = 'black'
            elif current_player == 0:
                self.current_player = 1
                self.current_team_points = 0
                self.current_player_colour = 'black'
        print(self.team_1_points, self.team_2_points)
        return(self.current_player)

    def perform_coin_in_hole(self, coins):
        for i in range (0, 19): #iterates through all coins on the board
            if coins[i].if_holed() == True and coins[i].get_holed() == False:
                #^checks if the coin is holed and not already removed
                coins[i].set_holed(True) #coin's holed attribute set to true
                coins[i].set_holed_temp(True)
                coins[i].remove() #coin removed from the board

    def holed_check(self, coins, current_player):
        redcoins = 0 # number of red coins holed
        mycoins = 0 #number of current player coins holed
        othercoins = 0 # number of other team coins holed
        change_player = False # change player originally false
        self.current_player = current_player
        for i in range(0,19): # iterates through all 19 coins on board
            if self.red_hit == False: # if the red coin hasn't been holed in previous turn
                if coins[i].get_holed_temp() == True and coins[i].getColour() == self.current_player_colour:
                    # ^(for each coin) if coin has been holed and is the current player's colour
                    mycoins = mycoins + 1 # mycoins increases by 1
                    print(coins[i].get_holed_temp())
                    coins[i].set_holed_temp(False)
                elif coins[i].get_holed_temp() == True and coins[i].getColour() != self.current_player_colour and coins[i].getColour() != 'red':
                    # ^ else if holed coin is not current player's coin and not red
                    othercoins = othercoins + 1 # othercoins increases by 1
                    coins[i].resetPosition(properties[i][0], properties[i][1]) #coin is placed back on board
                    coins[i].set_holed(False) #holed property of coin set to false
                    coins[i].set_holed_temp(False)
                elif coins[i].getColour() == 'red' and coins[i].get_holed_temp() == True: #else if red coin has been holed
                    redcoins = redcoins + 1 # redcoins increases by 1
                    coins[i].set_holed_temp(False) #this is where the issue is!!!!!!!!
            else: #else if the red coin had been holed in the previous turn
                if coins[i].get_holed_temp() == True and coins[i].getColour() == self.current_player_colour:
                    #^ if the holed coin is current player's colour
                    mycoins = mycoins + 1 # mycoins increases by 1
                    coins[i].set_holed_temp(False)
                elif coins[i].get_holed_temp() == True and coins[i].getColour() != self.current_player_colour and coins[i].getColour() != 'red':
                    #^ else if holed coin is not current player's coin and not red
                    othercoins = othercoins + 1 #othercoins increases by 1
                    coins[i].resetPosition(properties[i][0], properties[i][1]) #coin is placed back on board
                    print(coins[i].self.body.position)
                    coins[i].set_holed(False) #holed property of coin set to false
                    coins[i].set_holed_temp(False)
        if self.red_hit == False: #if red coin not holed in previous turn
            if redcoins > 0: #if red coin holed in this turn
                if mycoins >0: #if red coin and player's colour coin holed in this turn
                    self.current_team_points = self.current_team_points + 5 # player's points increase by 5
                    self.noofcoinsonboard = self.noofcoinsonboard - 1 - mycoins #number of coins on board decreases by number of coins holed
                    change_player = True # change player is true
                elif othercoins > 0: # else if red coin holed and other player's colour coin holed
                    coins[18].set_holed(False)
                    coins[18].set_holed_temp(False)
                    coins[18].resetPosition(properties[18][0], properties[18][1]) #red coin placed back in the middle of the board
                    change_player = True # change player is true
                elif mycoins == 0 and othercoins == 0: #else if red coin holed and no other coins holed
                    change_player = False #change player false (current player gets another turn)
                    self.red_hit = True #self.red_hit set to true
            else: #else if red coin hasn't been holed this turn
                if mycoins >0: # if current player's coins holed
                    self.current_team_points = self.current_team_points + mycoins #current player's points increase by number of coins holed
                    change_player = False # player gets another turn
                    self.noofcoinsonboard = self.noofcoinsonboard - mycoins # number of coins on board decreased by number of coins holed
                elif othercoins > 0: # else if other player's coins holed
                    change_player = True #player changes
                elif othercoins == 0 and mycoins == 0: #if no coins have been holed
                    change_player = True # player changes
        else: # if red coin holed in previous turn
            if mycoins > 0: # if player's coin holed in this turn
                self.red_hit = False # self.red_hit set to false
                change_player = True # player changes
                self.current_team_points = self.current_team_points + 5 #player's points increase by 5
                self.noofcoinsonboard = self.noofcoinsonboard - 1 - mycoins #number of coins on board decreases by number of coins holed
            elif othercoins > 0: # if other player's coin holed in this turn
                self.red_hit = False #self.red_hit set to false
                change_player = True #player changes
                coins[18].set_holed(False)
                coins[18].set_holed_temp(False)
                coins[18].resetPosition(properties[18][0], properties[18][1]) # red coin placed back on board
            elif mycoins == 0 and othercoins == 0: # if no coins have been holed
                self.red_hit = False #self.red_hit set to false
                change_player = True #player changes
                coins[18].set_holed(False)
                coins[18].set_holed_temp(False)
                coins[18].resetPosition(properties[18][0], properties[18][1]) # red coin placed back on board

        return change_player #returns true if player changes, false if player stays the same

    def player_strike(self,  current_player, coins, strikercoin):
        self.sliderpos.move() #moves the position slider to where the mouse clicked
        self.sliderforce.move() #moves force slider to where the mouse clicked
        self.directionslider.move() #moves direction slider to where the mouse clicked
        self.current_player = current_player #self.current player = current player passed in
        if CoinsMoving(coins, strikercoin ) == False: # if no coins are moving on the board
            self.StrikerCoin.changePos(self.sliderpos, self.current_player) # moves the striker coin to spcified position
        if self.Gobutton.CheckClicked(button_dimensions) == ('True') and CoinsMoving(coins, strikercoin ) == False :
            #^ if the strike button is clicked and no coins are moving
            self.StrikerCoin.moveStriker(self.sliderforce, self.directionslider, circle_base_dims) #striker is struck

    def end_round(self, coins):
        count1 = 0
        count2 = 0
        bool = False
        for i in range (0,9):
            if coins[i].get_holed() == True:
                count1 = count1 + 1
        for i in range(9,17):
            if coins[i].get_holed() == True:
                count2 = count2 + 1
        if count1 == 9:
            self.team_2_points = self.team_2_points + self.team_1_points
            for i in range(0,19):
                coins[i].resetPosition(properties[i][0], properties[i][1])
        if count2 == 9:
            self.team_1_points = self.team_1_points + self.team_2_points
            for i in range(0,19):
                coins[i].resetPosition(properties[i][0], properties[i][1])


def game():

#gamesetup
    for x in range(19):
        coin.append(Coin(properties[x][0], properties[x][1], 10, properties[x][2]))
        # creates 19 coins with the properties in the tuple listed above
        coin[x].set_holed(properties[x][3])
        # coin[x].limit_velocity()

    StrikerCoin = Coin(490, 590, 14, "white")
    StrikerCoin.set_holed(False)
    # StrikerCoin.limit_velocity()

    # the edges
    for e in edges_dimens:
        edges.append(Edges(e))
    for i in range(4):
        edges[i].draw()

    sliderpos = Slider(slider_position_dimensions, slider_position_bar_dimensions)
    sliderforce = Slider(slider_force_dimensions, slider_force_bar_dimensions)
    Gobutton = Button(button_dimensions)
    directionslider = Circular_Slider(80, circle_base_dims, circle_slide_dim, 10)

    noofplayers = 4
    newgame = Gamefunc(0, 2, 0, 0, 'black', 0, 0, 0, 0, 0, sliderpos, sliderforce, directionslider, StrikerCoin, Gobutton)

    current_player_local = 1
    noofplayers_local = noofplayers
    change = False
    player_struck = False


    # event handler
    while True:
        clock.tick(FPS)  # defines how often the space updates
        space.step(1 / FPS)  # space-time moved in steps using this function
        newgame.perform_coin_in_hole(coin) # removes any coin that falls in hole
        # changeplayerbool = newgame.holed(coin, current_player_local)
        # fill bgd
        screen.fill(BG)
        if not CoinsMoving(coin, StrikerCoin) and player_struck and not originalposition(coin) :
            # ^only performs the check once the coins have stopped moving, after a player has struck...
            # ... not originalposition(coin) : check does not happen before the first ever strike
            change = newgame.holed_check(coin, current_player_local) #if change is true, the player is changed
            player_struck = False # sets player_struck to false
            newgame.end_round(coin)
            if change:
                current_player_local = newgame.player_change(current_player_local) #changes player if change is true

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                newgame.player_strike(current_player_local, coin, StrikerCoin) #changes slider positions and strikes coin
                if Gobutton.CheckClicked(button_dimensions) == 'True': # if go button is clicked
                    player_struck = True #player struck set to true
                    # pygame.time.wait(1000)
            if event.type == pygame.QUIT:
                return
        board = Board()
        board.draw()
        space.debug_draw(options)
        pygame.display.update()


game()
pygame.quit()
