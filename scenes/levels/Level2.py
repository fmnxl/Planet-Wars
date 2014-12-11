import pygame
from lib.euclid import Vector2
from scenes.GameOverScene import GameOverScene
from models.Alien import Alien
from scenes.levels.Level import Level
from scenes.levels.Level3 import Level3

class Level2(Level):
	def __init__(self):
		super(Level2, self).__init__()
		self.num = 2

	def initialise(self):
		earth = self.planets[2]
		earth.setZone(5, 50, 10, self.probe)
		
		for i in [0,1,3]:
			planet = self.planets[i]
			self.aliens.append(Alien(planet.position + Vector2(3 + planet.size, 0), Vector2(0, 1.8), self.probe))
			self.aliens.append(Alien(planet.position + Vector2(7 + planet.size, 0), Vector2(0, 1.0), self.probe))

		self.instruction = "Defeat the aliens around the inner planets"

	def update(self, deltaTime):
		if len(self.aliens) == 0:
			self.manager.goTo(Level3())

	def handleEvents(self, events, keys):
		pass