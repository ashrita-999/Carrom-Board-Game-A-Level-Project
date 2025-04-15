import pymunk.pygame_util
import pygame
import pymunk
import math
from src.components.GameDimensions import GameDimensions


class CircularSlider:
    def __init__(self, base_radius, position_circle_base, position_circle_slide, circle_slide_radius, space):
        #defining base of circular slider
        self.space = space
        self.circle_base_position = position_circle_base
        self.circle_slide_base = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.circle_slide_base.position = ((self.circle_base_position[0],
                                            self.circle_base_position[1]))
        self.base_radius = base_radius
        self.slide_bar_holder_shape = pymunk.Circle(self.circle_slide_base, base_radius)
        self.space.add(self.circle_slide_base, self.slide_bar_holder_shape)

        self.circle_base_position = position_circle_base
        self.circle_slide_base2 = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.circle_slide_base2.position = ((self.circle_base_position[0], self.circle_base_position[1]))
        self.base_radius2 = base_radius - 8
        self.slide_bar_holder_shape2 = pymunk.Circle(self.circle_slide_base2, self.base_radius2)
        self.slide_bar_holder_shape2.color = (50, 50, 50, 50)
        self.space.add(self.circle_slide_base2, self.slide_bar_holder_shape2)

        # defining pointer of slider
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
        mouse_pos = pygame.mouse.get_pos()# coordinates of the cursor position
        x1 = self.circle_base_position[0]# x-coordinate of the centre of the circular base
        y1 = self.circle_base_position[1]#y coordinate of the centre of the circular base
        x = mouse_pos[0] - x1 # x coordinate of mouse click relative to the centre of the circular base
        y = mouse_pos[1] - y1# y coordinate of mouse click relative to the centre of the circular base

        # if the mouse click happened inside the circular base:
        if math.pow(x,2) + math.pow(y,2) < math.pow(self.base_radius, 2) or math.pow(x,2) + math.pow(y,2) == math.pow(self.base_radius, 2) :
            self.space.remove(self.circle_slide, self.circle_slide_shape)#removes previous instances of pointer
            self.posit_circle_slide = self.get_position().slidebar_dimensions# uses get_position method to draw the pointer
            self.circle_slide.position = ((self.posit_circle_slide[0], self.posit_circle_slide[1]))
            self.circle_slide_shape = pymunk.Circle(self.circle_slide, self.circle_slide_radius)
            self.circle_slide_shape.color = (255, 80, 100, 255)
            self.space.add(self.circle_slide, self.circle_slide_shape) # drawing the pointer

    def get_position(self):
        try:
            mouse_pos = pygame.mouse.get_pos()
            mouse_x = mouse_pos[0]# x-coordinate of mouse click
            mouse_y = mouse_pos[1] #y-coordinate of mouse click
            x1 = self.circle_base_position[0] # x-coordinate of centre of slider
            y1 = self.circle_base_position[1] # y-coordinate of centre of slider

            # angle of mouse click from horizontal
            angle = abs(math.atan((mouse_y - y1 ) / (mouse_x - x1)))

            # new x and y coordinates of pointer
            if mouse_x - x1 < 0:
                self.xpos =  x1 - self.base_radius*math.cos(angle)
            else :
                self.xpos = self.base_radius*math.cos(angle) + x1
            if mouse_y - y1 < 0:
                self.ypos = y1 - self.base_radius*math.sin(angle)
            else:
                self.ypos = y1 + self.base_radius*math.sin(angle)
            circle_slide_position = (self.xpos, self.ypos)
            self.current_dimensions = GameDimensions(circle_slide_position, angle)
        except:
            print("An exception occurred") #if division by 0 occurs
        return self.current_dimensions
    def draw(self, screen, imagepath, xscale, yscale, xpos, ypos ):
        self.screen = screen
        self.imagepath = imagepath
        #  load image
        self.table_image = pygame.image.load(imagepath).convert_alpha()

        #  scales image to board size
        self.table_imagereal = pygame.transform.scale(self.table_image, (xscale, yscale))
        self.screen.blit(self.table_imagereal, (xpos, ypos))
