import pygame


class Board:
    def __init__(self, screen):
        self.screen = screen
        #  load image
        self.table_image = pygame.image.load("/Users/ashri/git/carrom-board/src/assets/nusry-n-0RIEyCTxz4I-unsplash.jpg").convert_alpha()
        #  scales image to board size
        self.table_imagereal = pygame.transform.scale(self.table_image, (678, 678))

    def draw(self):
        # draws carrom board on the screen
        self.screen.blit(self.table_imagereal, (0, 0))

