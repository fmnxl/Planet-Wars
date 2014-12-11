import pygame
from lib.euclid import Vector2
from config.Config import *

class Level(object):
    def __init__(self):
        pass

    def initialise(self):
    	raise NotImplementedError

    def render(self, screen, camera):
		color = (0,254,253)
		font = pygame.font.Font(Config.getFile(Config.ethnocentric), 20)

		# # Level number indicator
		# text = font.render("LEVEL " + str(self.num), True, color)
		# textRect = text.get_rect()
		# textRect.topright = screen.get_rect().topright
		# textRect.right -= 20
		# textRect.top += 20
		# screen.blit(text, textRect)

		# instruction
		text = font.render(self.instruction, True, color)
		textRect = text.get_rect()
		textRect.centerx = screen.get_rect().centerx
		textRect.top = 20
		screen.blit(text, textRect)

    def update(self, deltaTime):
        raise NotImplementedError

    def handleEvents(self, events, keys):
        raise NotImplementedError