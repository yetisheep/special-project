import pygame
from pygame.locals import *


class Line:

    def __init__(self, screen, startP, endP, coord, color, url=None, width=3):	
        self.screen = screen
        self.startP = startP
        self.endP = endP
        self.coord = coord
        self.color = color
        self.url = url
        self.width = width

    def draw(self):
        self.screen.blit(self.url, self.coord)
