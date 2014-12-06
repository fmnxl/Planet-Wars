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
from scenes.levels.Level2 import *

class Level1(Level):
	def __init__(self):
		super(Level1, self).__init__()

	def initialise(self):
		earth = self.planets[2]
		jupiter = self.planets[4]
		earth.setZone(5, 50, 10, self.probe)
		
		self.probe.position = earth.position + Vector2(40,0)
		self.probe.speed =  Vector2(0,0)

		self.aliens.append(Alien(earth.position + Vector2(4,0), Vector2(0, 1.4), self.probe))
		self.aliens.append(Alien(earth.position - Vector2(8,0), Vector2(0, 0.8), self.probe))

	

	def update(self, deltaTime):
		if len(self.aliens) == 0 and self.probe.fuel >= self.probe.fuelCapacity:
			self.manager.goTo(Level2())

	def render(self, screen, camera):
		color = (0,254,253)
		if len(self.aliens) == 0 and self.probe.fuel >= self.probe.fuelCapacity:
			pass

		elif len(self.aliens) == 0:
			instruction = "Refuel your vehicle by going into earth's orbit"
		else:
			instruction = "Defeat the aliens around earth"

		font = pygame.font.Font(Config.getFile(Config.ethnocentric), 20)
		text = font.render(instruction, True, color)
		textRect = text.get_rect()
		textRect.centerx = screen.get_rect().centerx
		textRect.top = 20
		screen.blit(text, textRect)



	def handleEvents(self, events, keys):
		pass