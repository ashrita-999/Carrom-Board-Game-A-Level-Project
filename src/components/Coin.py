import pymunk.pygame_util
import pymunk
import math


class Coin:
    def __init__(self, x, y, coin_radius, colour, static_body, space, max_force):
        self.space = space
        self.holed_temp = False
        self.holed = False
        self.static_body = static_body
        self.body = pymunk.Body()  # defines the coin as a pymunk body
        self.body.position = x, y  # takes in x,y coords to position the body on the screen
        self.coin_radius = coin_radius  # takes in argument coin_radius to set the size of the coin
        self.shape = pymunk.Circle(self.body, coin_radius)  # sets the shape of the coin as a circle
        self.colour = colour
        if colour == "Red":
            self.shape.color = (255, 80, 100, 1)  # makes the coin red
        elif colour == "White":
            self.shape.color = (255, 255, 255, 1)  # makes the coin white
        elif colour == "Black":
            self.shape.color = (0, 0, 0, 1)  # makes the coin black
        elif colour == "Blue":
            self.shape.color = (0,0,255,1) # makes the coin red
        elif colour == "Yellow":
            self.shape.color = (255,255,0,1)  # makes the coin yellow
        elif colour == "Orange":
            self.shape.color = (255,127,80,1) # makes the coin orange
        elif colour == "Green":
            self.shape.color = (0,128,0,1) # makes the coin green
        self.shape.mass = 5  # unitless mass for coin
        self.pivot = pymunk.PivotJoint(static_body, self.body, (0, 0), (0, 0))  # using pivot joint for friction
        self.pivot.max_bias = 0  # disables joint correction
        self.pivot.max_force = max_force  # emulates linear friction
        self.shape.elasticity = 0.8

    def draw(self, space):
        space.add(self.body, self.shape, self.pivot)  # adds the coin to the screen

    def limit_velocity(self):
        # to prevent coins passing through edges
        self.max_velocity = 1000
        pymunk.Body.update_velocity(self.body, (0, 0), 1, 1)
        l = self.body.velocity.length
        if l > self.max_velocity:
            scale = self.max_velocity / l
            self.body.velocity = self.body.velocity * scale

    def changePos(self, slider, current_player):
        self.player = current_player
        if self.player == 1:  # bottom player
            x = (194 + ((( slider.current_dimensions.central_value - 805) / 547) * 283))  # gets the new y-coordinate of striker using position slider
            y = 490
        elif self.player == 2:  # next player clockwise (right-side player)
            x = 488
            y = (200 + (((slider.current_dimensions.central_value - 805) / 555) * 283))  # gets the new y-coordinate of striker using position slider
        elif self.player == 3:  # topmost player
            x = (194 + ((( slider.current_dimensions.central_value - 805) / 547) * 283))  # gets the new x-coordinate of striker using position slider
            y = 191
        elif self.player == 4:  # left-hand side player
            x = 186
            y = (200 + (((slider.current_dimensions.central_value - 805) / 555) * 283))  # gets the new x-coordinate of striker using position slider
        else:
            x = (194 + (((slider.current_dimensions.central_value - 805) / 547) * 283))  # gets the new y-coordinate of striker using position slider
            y = 490
        self.body.position = x, y  # changes the position of the striker to the x and y values specified

    def moveStriker(self, forcer, angle, centrepoint):

        #using force slider to calculate force value
        force = 1 * (((
                              forcer.current_dimensions.central_value - 805) / 543) * 283) * 80  # uses the force slider to calculate value of force

        x = 0
        y = 0
        xfixed = centrepoint[0] # x coord of centre of circular base
        yfixed = centrepoint[1] # y coord of centre of circular base

        #x and y positions of the pointer on the circular slider
        xslider = angle.current_dimensions.slidebar_dimensions[0]
        yslider = angle.current_dimensions.slidebar_dimensions[1]

        #determining direction of movement of striker

        #if mouse click happened to the right of the circular base's centre
        if xslider - xfixed > 0:
            x = force * math.cos(angle.current_dimensions.central_value)

        #if mouse click happened to the left of the circular base's centre
        elif xslider - xfixed < 0:
            x = -(force * math.cos(angle.current_dimensions.central_value))

        #if mouse click happened below circular base's centre
        if yslider - yfixed > 0:
            y = force * math.sin(angle.current_dimensions.central_value)

        #if mouse click happened above circular base's centre
        elif yslider - yfixed < 0:
            y = -(force * math.sin(angle.current_dimensions.central_value))
        self.body.apply_impulse_at_local_point((x, y), (0, 0))  # applies an impulse using the force specified

    def set_holed(self, holed):
        self.holed = holed

    def get_holed(self):
        return (self.holed)

    def set_holed_temp(self, tempholed):
        self.holed_temp = tempholed

    def get_holed_temp(self):
        return (self.holed_temp)

    def if_holed(self):
        bool = False
        x = self.body.position[0]  # the x-coordinate of the coin's position
        y = self.body.position[1]  # the y-coordinate of the coin's position
        if math.pow(x - 542, 2) + math.pow(y - 134, 2) <= math.pow(18, 2) \
                or math.pow(x - 123, 2) + math.pow(y - 132, 2) <= math.pow(18, 2) \
                or math.pow(x - 123, 2) + math.pow(y - 551, 2) <= math.pow(18, 2) \
                or math.pow(x - 551, 2) + math.pow(y - 549, 2) <= math.pow(18,
                                                                           2):  # if the coin lies within any of the holes, bool set to true
            bool = True
        return (bool)  # bool is only true if the coin is in the hole (i.e., coin is holed)

    def getColour(self):
        return (self.colour)

    def remove(self, space):
        space.remove(self.body, self.shape, self.pivot)

    def resetPosition(self, x, y, space):
        #resets position of coins to coordinates provided, sets their velocities to 0
        self.body.position = x, y
        self.body.velocity = (0, 0)
        space.add(self.body, self.shape, self.pivot)

    def setVelocity(self):
        self.body.velocity = (0, 0)
