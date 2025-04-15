import pygame


class EndGame:

    def __init__(self, screen):
        self.screen = screen
    def draw(self, screen, imagepath, xscale, yscale, xpos, ypos, bool ):
        if not bool == False:
            self.screen = screen
            self.imagepath = imagepath

            #  load image
            self.table_image = pygame.image.load(imagepath).convert_alpha()

            #  scales image to board size
            self.table_imagereal = pygame.transform.scale(self.table_image, (xscale, yscale))
            self.screen.blit(self.table_imagereal, (xpos, ypos))