import pygame
from pygame.locals import *


class Triangle:
    
	def __init__(self, screen, dot1, dot2, dot3, color, url, coord):	
		self.screen = screen
		self.dot1 = dot1
		self.dot2 = dot2
		self.dot3 = dot3
		self.color = color
		self.url = url
		self.coord = coord

	def draw(self):
                self.screen.blit(self.url, self.coord)
