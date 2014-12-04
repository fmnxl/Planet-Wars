import pygame, math, random
from lib.euclid import *
from models.Bullet import *

class Alien(object):
	def __init__(self, position, speed, enemy):
		self.position = position #Vector2(302.2,1)
		self.speed = speed #Vector2(-0.1,2.08)
		self.maxSpeed = 30
		self.maxSpeedSquared = self.maxSpeed ** 2
		self.thrust = 0.5
		self.fuelEfficiency = 0.1
		self.direction = 0
		self.gravitationalPull = Vector2(0,0)
		self.directionChange = 0
		self.maxHealth = 100
		self.health = self.maxHealth

		self.imageSize = Vector2(2,1)
		self.originalImage = pygame.image.load("img/ufo.png").convert_alpha()
		self.zoom = 0

		self.fuel = 100

		self.bullets = []

		self.fireRangeRadius = 16
		self.detectionRadius = 20

		self.fireTemp = 0
		self.isHit = False

		self.enemy = enemy
		self.alert = False

	def update(self, deltaTime):
		# deltaTimeSmall = deltaTime
		self.speed += self.gravitationalPull * deltaTime
		self.position += self.speed * deltaTime
		self.gravitationalPull = Vector2(0,0)
		self.direction += self.directionChange * deltaTime
		for bullet in self.bullets:

			bullet.update(deltaTime)
			if bullet.checkReach() == False:
				self.bullets.remove(bullet)

		if self.enemy is not None:
			self.fireAt(self.enemy)
			self.chase(self.enemy, deltaTime)
		
	def blit(self, screen, camera):
		if self.zoom != camera.zoom:
			self.zoomedImage = pygame.transform.scale(self.originalImage, map(int, (self.imageSize * camera.zoom)))
			self.tempImage = pygame.transform.rotate(self.zoomedImage, self.direction)
			self.rect = self.tempImage.get_rect()
			self.zoom = camera.zoom

		if abs(self.directionChange) > 0:
			oldCenter = self.rect.center
			self.tempImage = pygame.transform.rotate(self.zoomedImage, self.direction)
			self.rect = self.tempImage.get_rect()
			self.rect.center = oldCenter
			self.directionChange = 0

		if self.isHit:
			self.tempImage.fill((255,0,0), special_flags=pygame.BLEND_RGBA_MULT)

		self.rect.center = camera.convertCoordinates(self.position)
		screen.blit(self.tempImage, self.rect)

		if self.isHit:
			self.zoomedImage = pygame.transform.scale(self.originalImage, map(int, (self.imageSize * camera.zoom)))
			self.tempImage = pygame.transform.rotate(self.zoomedImage, self.direction)
			self.isHit = False

		maxWidth = 0.02 * camera.zoom  * self.maxHealth
		healthRect = pygame.Rect((self.rect.topleft), (maxWidth, 2))
		healthRect.bottom = self.rect.top - 4
		healthRect.centerx = self.rect.centerx
		oldLeft = healthRect.left

		healthRect.width = maxWidth * self.health / self.maxHealth
		healthRect.left = oldLeft
		pygame.draw.rect(screen, (0,255,0), healthRect, 0)

		font = pygame.font.Font("font/ethnocentric.ttf", int(round(0.4 * camera.zoom)))
		text = font.render("HP:" + str(self.health), True, (255,255,255))
		textRect = text.get_rect()
		textRect.left = healthRect.left
		textRect.bottom = healthRect.top - 1
		screen.blit(text, textRect)

		for bullet in self.bullets:
			bullet.blit(screen, camera)

	def fireAt(self, enemy):
		self.fireTemp += 1
		if (self.fireTemp) % 20 == 1:
			v = self.position - enemy.position
			if v.magnitude() <= self.fireRangeRadius:
				angle = math.degrees(math.atan2(v[0], v[1]))
				angle += random.randrange(-20, 20)
				bullet = Bullet(angle, self.position, self.speed, 50)
				self.bullets.append(bullet)

	def chase(self, enemy, deltaTime):
		v = enemy.position - self.position
		if self.alert or v.magnitude() <= self.detectionRadius:
			bv =  enemy.position - v.normalize() * 14
			v2bv = bv - self.position
			if v2bv.magnitude_squared() > 9:
				change = v2bv.normalize() * 3.0 * self.thrust
				self.position += change * deltaTime
				self.speed = change
			else:
				self.position += v2bv * deltaTime
				self.speed = Vector2(0,0)

	def checkBulletHit(self, other, camera):
		for bullet in self.bullets:
			if bullet.checkHit(other, camera):
				self.bullets.remove(bullet)