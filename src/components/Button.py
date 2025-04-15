import pygame
import pymunk


class Button:
    def __init__(self, dimens, space):
        #creating Pymunk static polygon for the button shape
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = ((0, 0))
        self.shape = pymunk.Poly(self.body, dimens)
        space.add(self.body, self.shape)

    def CheckClicked(self, initial_dimensions):
        #returns true if mouseclick happened inside the button
        self.mouse_pos = pygame.mouse.get_pos()
        if initial_dimensions[0][0] < self.mouse_pos[0] < initial_dimensions[2][0] and initial_dimensions[1][1] > self.mouse_pos[
            1] > initial_dimensions[2][1]:
            return ('True')
        else:
            return ('False')

    def draw(self, screen, imagepath, xscale, yscale, xpos, ypos ):
        self.screen = screen

        # get image path
        self.imagepath = imagepath

        #  load image
        self.button_label = pygame.image.load(imagepath).convert_alpha()

        #  scales image to board size
        self.button_label_real= pygame.transform.scale(self.button_label, (xscale, yscale))
        self.screen.blit(self.button_label_real, (xpos, ypos))

