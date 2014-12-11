import pygame, random
from lib.euclid import Vector2
from config.Config import Config
from models.Alien import Alien
from models.Planet import Planet
from models.Asteroid import Asteroid
from models.Probe import Probe
from scenes.levels.Level import Level
from scenes.levels.Level2 import Level2

class Level1(Level):
	def __init__(self):
		super(Level1, self).__init__()
		self.num = 1

	def initialise(self):
		earth = self.planets[2]
		earth.setZone(5, 50, 10, self.probe)
		
		self.probe.position = earth.position + Vector2(40,0)
		self.probe.fuel = 100

		self.aliens.append(Alien(earth.position + Vector2(4,0), Vector2(0, 1.4), self.probe))
		self.aliens.append(Alien(earth.position - Vector2(8,0), Vector2(0, 0.8), self.probe))

		self.instruction = "Defeat the aliens around earth"

	

	def update(self, deltaTime):
		if len(self.aliens) == 0 and self.probe.fuel >= self.probe.fuelCapacity:
			self.manager.goTo(Level2())
		elif len(self.aliens) == 0:
			self.instruction = "Refuel your vehicle by going into earth's orbit"
	

	def handleEvents(self, events, keys):
		pass