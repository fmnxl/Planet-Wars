import math, pygame, pygame.gfxdraw, random
from lib.euclid import *
from models.HeavenlyBody import HeavenlyBody
from config.Config import *

class Moon(HeavenlyBody):
	def __init__(self, size, mass, distance, period, imageFile, centerObject, angleToCenter):
		# basics and position
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
		self.originalImage = pygame.image.load(Config.getFile(imageFile)).convert_alpha()
		self.tempImage = pygame.transform.smoothscale(self.originalImage, map(int, (self.imageSize * self.zoom)))
		self.rect = self.tempImage.get_rect()

		self.update(0) # to calculate initial position


	def update(self, deltaTime):
		# position
		self.angleToCenter += deltaTime / self.period * math.radians(360)
		unitVector = Vector2(math.cos(self.angleToCenter), math.sin(self.angleToCenter))
		self.position = self.centerObject.position + self.distance * unitVector

	def blit(self, screen, camera):
		# draw orbital path
		converted = camera.convertCoordinates(self.centerObject.position)
		pygame.draw.circle(screen, (255,255,255), converted, int(round(self.distance * camera.zoom)), 1)

		converted = camera.convertCoordinates(self.position)

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
