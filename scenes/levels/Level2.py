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

	def initialise(self):
		planet = random.choice(self.planets)
		self.aliens.append(Alien(planet.position + Vector2(4,0), Vector2(0, 1.8), self.probe))
		self.aliens.append(Alien(planet.position + Vector2(8,0), Vector2(0, 1.0), self.probe))
		self.planetWithAliens = planet

	def render(self, screen, camera):
		color = (0,254,253)
		instruction = "Defeat the aliens around " + self.planetWithAliens.name

		font = pygame.font.Font(Config.getFile(Config.ethnocentric), 20)
		text = font.render(instruction, True, color)
		textRect = text.get_rect()
		textRect.centerx = screen.get_rect().centerx
		textRect.top = 20
		screen.blit(text, textRect)

	def update(self, deltaTime):
		if len(self.aliens) == 0:
			self.planetWithAliens.setZone(5, 50, 10, self.probe)
			self.manager.goTo(Level2())

	def handleEvents(self, events, keys):
		pass