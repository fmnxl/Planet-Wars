import pygame, math, pygame.mixer
from lib.euclid import *

class Bullet(object):
	def __init__(self, direction, position, initialSpeed, reach):
		self.direction = direction
		self.position = position
		self.originalPosition = position
		self.initialSpeed = initialSpeed
		self.reachSqauared = reach ** 2
		self.speed = 20.0
		self.damage = 1
		beep = pygame.mixer.Sound("sound/bullet.ogg")
		beep.play()

	def update(self, deltaTime):
		self.position -= Vector2(math.sin(math.radians(self.direction)), math.cos(math.radians(self.direction))) * self.speed * deltaTime
		self.position += self.initialSpeed * deltaTime
		
	def checkReach(self):
		return (self.position - self.originalPosition).magnitude_squared() <= self.reachSqauared			

	def blit(self, screen, camera):
		bulletCoordinate = camera.convertCoordinates(self.position)
		pygame.draw.circle(screen, (255,255,255), map(int, bulletCoordinate), int(round(0.07* camera.zoom)) , 0)

	def checkHit(self, other, camera):
		if other.rect.collidepoint(camera.convertCoordinates(self.position)):
			other.health -= self.damage
			other.isHit = True
			return True
		return False