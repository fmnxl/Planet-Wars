import math, pygame, pygame.gfxdraw, random
from lib.euclid import *
from models.HeavenlyBody import HeavenlyBody

class Planet(HeavenlyBody):
	def __init__(self, name, size, mass, distance, period, imageFile, centerObject, angleToCenter):
		# basics and position
		self.name = name
		self.position = Vector2(0,0)
		self.size = size
		self.mass = mass
		self.distance = distance
		self.period = period
		self.centerObject = centerObject
		self.angleToCenter = angleToCenter

		# images
		self.imageSize = Vector2(size*2, size*2)
		self.zoom = 0
		self.minZoom = 10
		self.originalImage = pygame.image.load(imageFile).convert_alpha()
		self.tempImage = pygame.transform.smoothscale(self.originalImage, map(int, (self.imageSize * self.zoom)))
		self.rect = self.tempImage.get_rect()

		# zone
		self.zoneRadius = 0
		self.fuelingRate = 0
		self.healingRate = 0
		self.objectToHealOrFuel = None

		self.moons = []
		self.mines = []

		self.update(0) # to calculate initial position

	def setZone(self, radius, fuelingRate, healingRate, objectToHealOrFuel):
		self.zoneRadius = radius
		self.fuelingRate = fuelingRate
		self.healingRate = healingRate
		self.objectToHealOrFuel = objectToHealOrFuel

	def update(self, deltaTime):
		# position
		self.angleToCenter += deltaTime / self.period * math.radians(360)
		unitVector = Vector2(math.cos(self.angleToCenter), math.sin(self.angleToCenter))
		self.position = self.centerObject.position + self.distance * unitVector

		# healing or fueling
		if self.zoneRadius > 0 and self.objectToHealOrFuel is not None:
			self.healOrFuel(self.objectToHealOrFuel, deltaTime)

		for moon in self.moons:
			moon.update(deltaTime)

		for mine in self.mines:
			mine.update(deltaTime)

	def blit(self, screen, camera):
		# draw orbital path if zoom is not too large
		if(camera.zoom <= 35.0):
			converted = camera.convertCoordinates(self.centerObject.position)
			pygame.draw.circle(screen, (255,255,255), converted, int(round(self.distance * camera.zoom)), 1)

		converted = camera.convertCoordinates(self.position)

		# draw healing / fueling radius
		if self.zoneRadius > 0:
			#pygame.draw.circle(screen, (50,255,50), converted, int(round(self.fuelingRadius * camera.zoom)) , 0)
			try:
				pygame.gfxdraw.aacircle(screen, converted.x, converted.y, int(round(self.zoneRadius * camera.zoom)), (50,255,50, 50))
				pygame.gfxdraw.filled_circle(screen, converted.x, converted.y, int(round(self.zoneRadius * camera.zoom)), (50,255,50, 50))	
			except:
				pass

		# draw planet
		#pygame.draw.circle(screen, self.colour, converted, int(round(self.size * camera.zoom)) , 0)
		# try:
		# 	zoom = int(round(self.size * camera.zoom))
		# 	if(zoom < 4):
		# 		zoom = 4
		# 	pygame.gfxdraw.aacircle(screen, converted.x, converted.y, zoom, self.colour)
		# 	pygame.gfxdraw.filled_circle(screen, converted.x, converted.y, zoom, self.colour)	
		# except:
		# 	pass
		if self.zoom != camera.zoom:
			zoom = map(int, map(round, self.imageSize * camera.zoom))
			
			minMinZoom = int(round(self.minZoom * self.size))
			if zoom[0] < self.minZoom < minMinZoom:
				zoom = Vector2(self.minZoom,self.minZoom)
			elif zoom[0] < minMinZoom < self.minZoom:
				zoom = Vector2(minMinZoom,minMinZoom)

			self.tempImage = pygame.transform.scale(self.originalImage, zoom)
			self.rect = self.tempImage.get_rect()
			self.zoom = camera.zoom

		self.rect.center = map(round, camera.convertCoordinates(self.position))
		screen.blit(self.tempImage, self.rect)

		for moon in self.moons:
			moon.blit(screen, camera)

		for mine in self.mines:
			mine.blit(screen, camera)

	def healOrFuel(self, object, deltaTime):
		# validation: has to be within zone
		if (self.position - object.position).magnitude() > self.zoneRadius:
			return

		# fuel
		if self.fuelingRate > 0 and object.fuel < object.fuelCapacity and object.acceleration == Vector2(0,0): 
			object.fuel += self.fuelingRate * deltaTime

		# heal
		if self.healingRate > 0 and object.health < object.maxHealth and object.acceleration == Vector2(0,0): 
			object.health += self.healingRate * deltaTime