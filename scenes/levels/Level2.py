import pygame, math, random, pygame.gfxdraw, sys
from pygame.locals import *
from lib.euclid import *
from config.Config import *
from scenes.Scene import *
from scenes.GameOverScene import GameOverScene
from models.Alien import *
from models.Camera import *
from models.Planet import *
from models.Asteroid import *
from models.Probe import *
from models.Sun import *
from scenes.levels.Level import *

class Level2(Level):
	def __init__(self):
		super(Level2, self).__init__()
		pass

	def initialise(self):
		mars = self.planets[4]
		self.aliens.append(Alien(mars.position + Vector2(4,0), Vector2(0, 1.8), self.probe))
		self.aliens.append(Alien(mars.position + Vector2(8,0), Vector2(0, 1.0), self.probe))

	def render(self, screen, camera):
		color = (0,254,253)
		if len(self.aliens) == 0 and self.probe.fuel >= self.probe.fuelCapacity:
			pass

		elif len(self.aliens) == 0:
			font = pygame.font.Font("font/ethnocentric.ttf", 20)
			text = font.render("Now refuel your vehicle", True, color)
			textRect = text.get_rect()
			textRect.centerx = screen.get_rect().centerx
			textRect.top = 20
			screen.blit(text, textRect)
		else:
			font = pygame.font.Font("font/ethnocentric.ttf", 20)
			text = font.render("Destroy the aliens around mars", True, color)
			textRect = text.get_rect()
			textRect.centerx = screen.get_rect().centerx
			textRect.top = 20
			screen.blit(text, textRect)

	def update(self, deltaTime):
		pass

	def handleEvents(self, events, keys):
		pass