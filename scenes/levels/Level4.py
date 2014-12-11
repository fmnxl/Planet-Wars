import pygame
from lib.euclid import Vector2
from scenes.GameOverScene import GameOverScene
from models.Alien import Alien
from scenes.levels.Level import Level

class Level4(Level):
	def __init__(self):
		super(Level4, self).__init__()
		self.num = 4
		self.instruction = "Defeat the aliens around the outer planets"

	def initialise(self):
		self.probe.fuelCapacity = 4000
		self.probe.maxSpeed = 30
		self.probe.maxSpeedSquared = self.probe.maxSpeed ** 2

		for i in [0,1,2,3]:
			planet = self.planets[i]
			planet.setZone(5, 50, 10, self.probe)

		for i in range(4,6):
			planet = self.planets[i]
			self.aliens.append(Alien(planet.position + Vector2(3 + planet.size, 0), Vector2(0, 1.8), self.probe))
			self.aliens.append(Alien(planet.position + Vector2(7 + planet.size, 0), Vector2(0, 1.0), self.probe))		

	def update(self, deltaTime):
		if len(self.aliens) == 0:
			for i in range(4,6):
				planet = self.planets[i]
				planet.setZone(5, 50, 10, self.probe)
			self.manager.goToWinScene()

	def handleEvents(self, events, keys):
		pass