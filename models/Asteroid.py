import math, pygame, pygame.gfxdraw
from lib.euclid import *
from models.HeavenlyBody import HeavenlyBody

class Asteroid(HeavenlyBody):
	def __init__(self, size, mass, distance, period, colour, centerObject, angleToCenter):
		self.position = Vector2(0,0)
		self.size = size
		self.mass = mass
		self.distance = distance
		self.period = period
		self.colour = colour
		self.centerObject = centerObject
		self.angleToCenter = angleToCenter
		self.fuel = False

	def update(self, deltaTime):
		self.angleToCenter += deltaTime / self.period * math.radians(360)
		unitVector = Vector2(math.cos(self.angleToCenter), math.sin(self.angleToCenter))
		self.position = self.centerObject.position + self.distance * unitVector

	def blit(self, screen, camera):
		converted = camera.convertCoordinates(self.position)

		# draw planet
		#pygame.draw.circle(screen, self.colour, converted, int(round(self.size * camera.zoom)) , 0)
		try:
			zoom = int(round(self.size * camera.zoom))
			if(zoom < 2):
				zoom = 2
			pygame.gfxdraw.aacircle(screen, converted.x, converted.y, zoom, self.colour)
			pygame.gfxdraw.filled_circle(screen, converted.x, converted.y, zoom, self.colour)	
		except:
			pass