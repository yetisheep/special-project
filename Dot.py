import pygame
from pygame.locals import *

BLACK = (0, 0, 0)
dot_pic = pygame.image.load("image/dot.png")
offset = 10

class Dot:
    
        def __init__(self, screen, i, coord):	
                self.screen = screen
                self.i = i
                self.coord = coord
                self.color = BLACK
                self.radius = 15

        def draw(self):
                self.screen.blit(dot_pic, [self.coord[0]-offset, self.coord[1]-offset])
