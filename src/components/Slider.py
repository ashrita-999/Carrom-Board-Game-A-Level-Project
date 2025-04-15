import pygame
import pymunk

from src.components.GameDimensions import GameDimensions


class Slider:
    def __init__(self, dimensions_base, dimensions_bar, space):
        self.space = space
        self.initial_dimensions = dimensions_base # sets dimensions of base of slider
        self.slide_base = pymunk.Body(body_type=pymunk.Body.STATIC) # sets slider base to a static object
        self.slide_base.position = ((0, 0))
        self.slide_bar_holder_shape = pymunk.Poly(self.slide_base, self.initial_dimensions) #sets slider base as 'poly' (4 vertices)
        self.space.add(self.slide_base, self.slide_bar_holder_shape) #adds slider base to the space

        self.initial_bar_dimensions = dimensions_bar # sets dimensions of sliding bar
        self.slide_bar = pymunk.Body(body_type=pymunk.Body.STATIC) # sets sliding bar as a static body
        self.slide_bar.position = ((0, 0))
        self.current_dimensions = self.get_dimensions() # current_dimensions is used instead of a global variable to be able to move the striker (used in coin.changePos)
        self.dimens_bar = self.current_dimensions.slidebar_dimensions # sets dimens_bar to the current position of sliding bar using current_dimensions attribute
        self.slide_bar_shape = pymunk.Poly(self.slide_bar, self.dimens_bar) # sets sliding bar shape as a 'Poly' (4 vertices)
        self.slide_bar_shape.color = (255, 80, 100, 255) #sets colour of sliding bar to red
        self.space.add(self.slide_bar, self.slide_bar_shape) #adds sliding bar to the screen

    def move(self):
        mouse_pos = pygame.mouse.get_pos() #mouse_pos set to x and y coordinates of the current mouse position
        if self.initial_dimensions[0][0] < mouse_pos[0] < self.initial_dimensions[2][0] \
                and self.initial_dimensions[1][1] > mouse_pos[1] > self.initial_dimensions[2][1]  :
            self.space.remove(self.slide_bar, self.slide_bar_shape) # removes previous instances of the sliding bar
            self.dimens_bar = self.get_dimensions().slidebar_dimensions # sets the dimensions of the bar using the get_dimensions method
            self.slide_bar_shape = pymunk.Poly(self.slide_bar, self.dimens_bar) # sets sliding bar as a 'Poly' shape (4 vertices)
            self.slide_bar_shape.color = (255, 80, 100, 255) # sets sliding bar's colour to red
            self.space.add(self.slide_bar, self.slide_bar_shape) #adds new instance of sliding bar to the screen

    def get_dimensions(self):
        mouse_pos = pygame.mouse.get_pos() #gets the mouse position of the screen
        mouse_x = mouse_pos[0] #sets mouse_x to the x-coordinate of mouse-position
        y = (self.initial_dimensions[0][1] + self.initial_dimensions[1][1]) / 2
        x = mouse_pos[0]
        avgx = (self.initial_bar_dimensions[2][0] - self.initial_bar_dimensions[0][0]) / 2
        avgy = (self.initial_bar_dimensions[1][1] - self.initial_bar_dimensions[0][1]) / 2
        slider_bar_dimens = (x - avgx, y + avgy), (x - avgx, y - avgy), (x + avgx, y + avgy), (x + avgx, y - avgy)
        self.current_dimensions = GameDimensions(slider_bar_dimens, mouse_x) # uses the GameDimension utility class to return slider_bar_dimens and mouse_x both
        return self.current_dimensions

    def draw(self, screen, imagepath, xscale, yscale, xpos, ypos ):
        #drawing labels of buttons
        self.screen = screen
        self.imagepath = imagepath

        #  load image
        self.table_image = pygame.image.load(imagepath).convert_alpha()

        #  scales image
        self.table_imagereal = pygame.transform.scale(self.table_image, (xscale, yscale))
        self.screen.blit(self.table_imagereal, (xpos, ypos))
