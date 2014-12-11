import pygame
from scenes.levels.Level import Level
from scenes.levels.Level4 import Level4

class Level3(Level):
	def __init__(self):
		super(Level3, self).__init__()
		self.num = 3
		self.instruction = "Cross the asteroid belt"

	def initialise(self):
		self.probe.fuelCapacity = 4000
		self.probe.maxSpeed = 30
		self.probe.maxSpeedSquared = self.probe.maxSpeed ** 2

		for i in [0,1,2,3]:
			planet = self.planets[i]
			planet.setZone(5, 50, 10, self.probe)


	def update(self, deltaTime):
		if self.probe.position.magnitude_squared() > 600**2:
			self.manager.goTo(Level4())

	def handleEvents(self, events, keys):
		pass