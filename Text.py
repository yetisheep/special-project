import pygame
from pygame.locals import *


class Text:

    def __init__(self, screen, str, color, font, coord):				
        self.screen = screen
        self.str = str
        self.color = color
        self.font = font
        self.coord = coord

    def draw(self):
        text = self.font.render(self.str, True, self.color)
        self.screen.blit(text, self.coord)
		
	
