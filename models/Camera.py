import pygame
from lib.euclid import *

class Camera(object):
	def __init__(self, screenSize):
		# self.minZoom = float(screenSize[1]) / float(observableUniverse[1]) + 1
		self.minZoom = 0.0
		self.maxZoom = 55.0
		self.zoom = 20.0
		self.center = Vector2(0, 0)
		self.speed = Vector2(0, 0)
		self.maxSpeed = 200
		self.acceleration = 40
		self.deceleration = 600
		self.screenSize = screenSize
		self.dontSlowDownCamera = False
		self.topleft = self.center - self.screenSize * (0.5 / self.zoom)
		self.lockCameraToProbe = True


	def slowDown(self, speed, factor, deltaTime):
		slowDownChange = factor * deltaTime
		if(speed > 0):
			if(speed >= slowDownChange):
				speed -= slowDownChange
			else:
				speed = 0
		elif(speed < 0):
			if(speed < -slowDownChange):
				speed += slowDownChange
			else:
				speed = 0
		return speed

	def slowDownVector(self, speed, factor, deltaTime):
		return Vector2(self.slowDown(speed[0], factor, deltaTime), self.slowDown(speed[1], factor, deltaTime))

	def convertCoordinatesParallax(self, coordinates, z):
		v = coordinates - self.center * z + self.screenSize / 2
		v = v
		return v

	def convertCoordinates(self, coordinates):
		v = (coordinates - self.topleft) * self.zoom
		v[0] = int(round(v[0]))
		v[1] = int(round(v[1]))
		return v

	def listenToKeyboard(self, keys, events):
		for event in events:
			if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
				self.lockCameraToProbe = not self.lockCameraToProbe

		if keys[pygame.K_LEFT]:
			if self.speed[0] > 0:
				self.speed[0] = 0
			self.speed[0] -= self.acceleration / self.zoom if self.speed[0] > -self.maxSpeed / self.zoom else 0
			self.dontSlowDownCamera = True
		if keys[pygame.K_RIGHT]:
			if self.speed[0] < 0:
				self.speed[0] = 0
			self.speed[0] += self.acceleration / self.zoom if self.speed[0] < self.maxSpeed / self.zoom else 0
			self.dontSlowDownCamera = True
		if keys[pygame.K_UP]:
			if self.speed[1] > 0:
				self.speed[1] = 0
			self.speed[1] -= self.acceleration / self.zoom if self.speed[1] > -self.maxSpeed / self.zoom else 0
			self.dontSlowDownCamera = True
		if keys[pygame.K_DOWN]:
			if self.speed[1] < 0:
				self.speed[1] = 0
			self.speed[1] += self.acceleration / self.zoom if self.speed[1] < self.maxSpeed / self.zoom else 0
			self.dontSlowDownCamera = True
		

		if keys[pygame.K_MINUS]:
			if self.zoom > self.minZoom:
				self.zoom = self.zoom * 0.95
		if keys[pygame.K_EQUALS]:
			if self.zoom < self.maxZoom:
				self.zoom = self.zoom * 1.05

	def update(self, deltaTime, probe):
		if self.lockCameraToProbe:
			self.center = probe.position
			self.topleft = self.center - self.screenSize * (0.5 / self.zoom)
			self.speed = Vector2(0,0)
			return
		if self.dontSlowDownCamera == False:
			self.speed = self.slowDownVector(self.speed, self.deceleration, deltaTime)
		self.center = self.center + self.speed * deltaTime
		self.topleft = self.center - self.screenSize * (0.5 / self.zoom)
		self.dontSlowDownCamera = False